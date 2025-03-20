"""The module provides classes to deal with different types of measurements."""

from __future__ import annotations

import contextlib
import copy
import logging
from abc import ABC, abstractmethod
from functools import cached_property
from itertools import cycle
from typing import Any, Iterable

import numpy as np
import numpy.typing as npt

from daxs.interpolators import Interpolator2D
from daxs.scans import Scan, Scans
from daxs.sources import Source
from daxs.utils.arrays import trapezoid

logger = logging.getLogger(__name__)


class ConcentrationCorrectionError(Exception):
    def __init__(self, message: str):
        super().__init__(f"{message} The concentration correction failed.")


class Corrector(ABC):
    """Base class for measurement correctors."""

    @abstractmethod
    def apply(self, scans: Scans) -> None:
        """Apply the correction to the scans."""


class SimpleConcentrationCorrector(Corrector):
    """Class to perform simple, length-based, concentration corrections."""

    def __init__(self, scans: Scan | Scans):
        """
        Parameters
        ----------
        scans :
            Scans used for concentration correction.
        """
        self.conc_corr_scans = scans if isinstance(scans, Scans) else Scans([scans])

    def apply(self, scans: Scans) -> None:
        logger.info("Applying simple concentration correction.")
        # When there is a single concentration correction scan and the number
        # of points in it is equal to the number of scans to be corrected, each
        # point will be used to correct a scan.
        if len(self.conc_corr_scans) == 1:
            [conc_corr_scan] = self.conc_corr_scans
            if len(scans) == conc_corr_scan.signal.size:
                for i, scan in enumerate(scans):
                    try:
                        scalars = (conc_corr_scan.signal[i], conc_corr_scan.monitor[i])
                    except IndexError:
                        scalars = (conc_corr_scan.signal[i],)
                    scan.divide_by_scalars(*scalars)
                return

        # When there is a single concentration correction scan and the previous
        # condition is not met, divide all scans by it, by cycling it.
        if len(self.conc_corr_scans) == 1:
            conc_corr_scans = cycle(self.conc_corr_scans)

        # When the number of scans to be corrected is equal to the number of
        # concentration correction scans, each scan will be corrected by a
        # corresponding concentration correction scan.
        elif len(self.conc_corr_scans) == len(scans):
            conc_corr_scans = self.conc_corr_scans
        # No other case is supported.
        else:
            raise ConcentrationCorrectionError(
                "Incompatible number of scans to correct and concentration "
                "correction scans."
            )

        for scan, conc_corr_scan in zip(scans, conc_corr_scans):
            try:
                scan.divide_by_scan(conc_corr_scan)
            except (TypeError, ValueError) as e:
                raise ConcentrationCorrectionError(
                    f"The length of the signal or monitor in the scan {scan.label} "
                    "is different than that from the correction scan "
                    f"{conc_corr_scan.label}."
                ) from e


class DataDrivenConcentrationCorrector(Corrector):
    """Class to perform concentration corrections using data from specified paths."""

    def __init__(self, scans: Scan | Scans, paths: dict[str, str]):
        """
        Parameters
        ----------
        scans :
            Scans used for concentration correction.
        paths :
            Paths to the concentration correction data. It assumes they are the
            same for specified scans.
        """
        self.conc_corr_scans = scans if isinstance(scans, Scans) else Scans([scans])
        self.paths = paths

    @cached_property
    def conc_corr_points(self) -> npt.NDArray[np.float64]:
        """
        Array of points used to determine the concentration correction indices.

        Returns
        -------
        npt.NDArray[np.float64]
            Array of points used for concentration correction.

        Raises
        ------
        ValueError
            If the concentration correction counters don't have the same length.
        """
        points = []
        for path in self.paths.values():
            points_at_path = []
            for conc_corr_scan in self.conc_corr_scans:
                points_at_path.extend(conc_corr_scan.read_data_at_paths(path))
            points.append(points_at_path)

        try:
            return np.asarray(points, dtype=np.float64).T
        except ValueError as e:
            raise ConcentrationCorrectionError(
                "The concentration correction counters must have the same length."
            ) from e

    def find_conc_corr_indices(self, scan: Scan) -> list[int]:
        """
        Determine the indices of the concentration correction data for each point in
        the scan.

        Parameters
        ----------
        scan :
            Scan for which the concentration correction data indices are to be found.

        Returns
        -------
        list[int]
            Indices of the concentration correction data for the points in the scan.
        """
        # Get concentration correction points.
        conc_corr_points = self.conc_corr_points
        # conc_corr_points[-1, :] = conc_corr_points[80, :]

        # Get the scan data at the same keys as the concentration correction data.
        data_points = []
        for key in self.paths:
            try:
                data_points.append(scan.data[key])
            except KeyError as e:
                raise ConcentrationCorrectionError(
                    f"The data in scan {scan.label} does not have the key {key} among"
                    "the source data paths. Make sure the source data paths are"
                    "correctly set."
                ) from e
        # data_points = [
        #     [8.6775, 8.82, 8.9625],
        #     [-10.63, -10.63, -10.63],
        # ]
        data_points = np.asarray(data_points)
        # Add a new axis if the data points are 1D.
        if data_points.ndim == 1:
            data_points = data_points[:, None]
        # Transpose the data points to have shape (N, p) [N points, p paths].
        data_points = data_points.T

        # Calculate distances between each data point and each concentration correction
        # point.
        # data_points has shape (N, p) [N points, p paths]
        # data_points[:, None, :] has shape (N, 1, p)
        # conc_corr_points has shape (M, p) [M points, p paths]
        # conc_corr_points[None, :, :] has shape (1, M, p) [M points]
        # The subtraction uses broadcasting to yield an array of shape (N, M, p),
        # np.linalg.norm(..., axis=2) computes the Euclidean distance resulting in an
        # array of shape [N, M].

        distances = np.linalg.norm(
            data_points[:, None, :] - conc_corr_points[None, :, :],
            axis=2,
        )

        threshold = np.finfo(np.float64).eps
        # For each data point, find the index where the distance is smaller
        # than the threshold. If the number of indices is different than 1, raise an
        # error.
        mask = distances < threshold
        if np.any(mask.sum(axis=1) != 1):
            raise ConcentrationCorrectionError(
                "There must be a single concentration correction point for each data "
                "point."
            )
        _, indices = np.where(mask)
        return indices.tolist()

    def create_conc_corr_scan(self, indices: list[int]) -> Scan:
        """
        Create a scan with the concentration correction data at the specified indices.

        Parameters
        ----------
        indices :
            Indices of the concentration correction data to be used.

        Returns
        -------
        Scan
            Scan with the concentration correction data at the specified indices.
        """
        signal = np.concatenate([scan.signal for scan in self.conc_corr_scans])
        scan = Scan(None, signal[indices])

        try:
            monitor = np.concatenate([scan.monitor for scan in self.conc_corr_scans])
            scan.monitor = monitor[indices]
        except IndexError:
            pass
        return scan

    def apply(self, scans: Scans) -> None:
        """
        Apply the concentration correction using data from the specified paths.

        Parameters
        ----------
        scans :
            Scans to be corrected.
        """
        logger.info("Applying data-informed concentration correction.")
        for scan in scans:
            indices = self.find_conc_corr_indices(scan)
            conc_corr_scan = self.create_conc_corr_scan(indices)
            scan.divide_by_scan(conc_corr_scan)


class DeadTimeCorrector(Corrector):
    """Class to perform dead time corrections."""


class Measurement:
    """Base class for measurements."""

    def __init__(self, sources: Source | list[Source]):
        """
        Parameters
        ----------
        sources :
            Sources of scans.
        """
        self.sources = [sources] if isinstance(sources, Source) else sources

        self._scans: Scans | None = None
        self._x: npt.NDArray[np.float64] = np.array([])
        self._signal: npt.NDArray[np.float64] = np.array([])
        self._monitor: npt.NDArray[np.float64] = np.array([])

    @property
    def scans(self) -> Scans:
        """The scans of the measurement."""
        if self._scans is None:
            self._scans = Scans()
            for source in self.sources:
                self._scans.extend(source.scans)

            if len(self._scans) == 0:
                raise ValueError("The measurement has no scans.")

            self._scans.check_sizes()

            self._x = np.array([])
            self._signal = np.array([])
            self._monitor = np.array([])
        return self._scans

    def add_source(self, source: Source) -> None:
        """
        Add a new source to the measurement.

        Parameters
        ----------
        source :
            Source to be added.
        """
        self.sources.append(source)
        self._scans = None

    def remove_source(self, index: int) -> None:
        """
        Remove a source from the measurement.

        Parameters
        ----------
        index :
            Index of the source to be removed.
        """
        self.sources.pop(index)
        self._scans = None

    def add_scans(self, scans: Scan | list[Scan]) -> None:
        """
        Add scans to the measurement.

        Parameters
        ----------
        scans :
            Scans to be added.
        """
        scans = [scans] if isinstance(scans, Scan) else scans

        if self._scans is None:
            self._scans = Scans()

        for scan in scans:
            self._scans.append(scan)
            logger.debug("Scan %s was added.", scan.label)

    def remove_scans(
        self, indices: int | list[int], filename: str | None = None
    ) -> None:
        """
        Remove scans from the measurement.

        Parameters
        ----------
        indices :
            Indices of the scans to be removed.
        filename :
            Name of the file from which the scans where read.
        """
        indices = [indices] if isinstance(indices, int) else indices

        for index in indices:
            for scan in self.scans:
                if index == scan.index and (
                    filename is None or scan.filename == filename
                ):
                    self.scans.remove(scan)
                    logger.debug("Scan %s was removed.", scan.label)

    def reset(self, scans: float = True):
        """Reset the measurement."""
        self._x, self._signal, self._monitor = np.array([]), np.array([]), np.array([])
        if scans:
            self.scans.reset()

    def get_scans(
        self, indices: int | list[int], filename: str | None = None
    ) -> list[Scan]:
        indices = [indices] if isinstance(indices, int) else indices

        scans = []
        for index in indices:
            for scan in self.scans:
                if scan.index == index and (
                    filename is None or scan.filename == filename
                ):
                    scans.append(scan)

        return scans

    # TODO: Should the method also accept an argument that limits the scans which
    # will be corrected?
    def concentration_correction(
        self,
        indices: int | list[int] | npt.NDArray[np.int64] | None = None,
        scans: Scan | list[Scan] | Scans | None = None,
        paths: dict[str, str] | None = None,
    ) -> None:
        """Apply the concentration correction using data from the specified scans.

        Parameters
        ----------
        indices :
            Indices of the scans used for concentration correction.
        scans :
            Scans used for concentration corrections.
        paths :
            Paths used to locate the required concentration correction data.
        """
        # Get the scans to be used for concentration correction.
        if indices is not None:
            indices = [indices] if isinstance(indices, int) else indices

            source = copy.deepcopy(self.sources[0])
            data_mappings = copy.deepcopy(source.data_mappings)

            with contextlib.suppress(KeyError):
                data_mappings["x"] = ".1/measurement/elapsed_time"
                logger.debug(
                    "The X-axis mapping for the concentration "
                    "correction scans was updated to elapsed time."
                )

            source.data_mappings = data_mappings
            scans = source.read_scans(indices)
        elif scans is not None:
            pass
        else:
            raise ValueError("Either the indices or scans must be specified.")

        conc_corr_scans = scans if isinstance(scans, Scans) else Scans(scans)

        if paths is None:
            corrector = SimpleConcentrationCorrector(conc_corr_scans)
        else:
            corrector = DataDrivenConcentrationCorrector(conc_corr_scans, paths)
        corrector.apply(self.scans)

        # Force signal and monitor reevaluation.
        self._signal, self._monitor = np.array([]), np.array([])


class Measurement1D(Measurement):
    """Base class for 1D measurements."""

    @property
    def x(self):
        if self._x.size == 0:
            self._x = self.scans.get_common_axis()
            # Assign the common axis to the scans.
            for scan in self.scans:
                scan.x = self._x
        return self._x

    @x.setter
    def x(self, a: npt.NDArray[np.float64]):
        logger.info("Setting new x-axis.")
        for scan in self.scans:
            scan.x = a
        self._x = a
        self._signal, self._monitor = np.array([]), np.array([])

    @property
    def signal(self):
        if self._signal.size == 0:
            self.process()
        return self._signal

    @property
    def monitor(self):
        if self._monitor.size == 0:
            self.process()
        return self._monitor

    def find_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Find outliers in the data.

        See the docstring of :meth:`.scans.Scan.find_outliers`.
        """
        for scan in self.scans:
            scan.find_outliers(method=method, **kwargs)

    def remove_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Remove outliers from the signal.

        See the docstring of :meth:`.scans.Scan.remove_outliers`.
        """
        logger.info("Removing outliers.")
        for scan in self.scans:
            scan.remove_outliers(method=method, **kwargs)
        self._signal = np.array([])

    def process(
        self, aggregation: str = "fraction of sums", normalization: str | None = None
    ):
        """
        Process the scans data.

        The processing includes aggregating the data of the selected scans
        and normalizing the signal.
        """
        self.aggregate(mode=aggregation)
        if normalization is not None:
            self.normalize(mode=normalization)

    def aggregate(self, mode: str = "fraction of sums"):
        """
        Aggregate the scans signal using the selected mode.

        When present, the aggregated monitor is always a sum of the monitors from
        the individual scans.

        Parameters
        ----------
        mode : str
            Defines how the signal is aggregated.

                - "sum" : Sum of the signals from all scans.
                - "fraction of sums" : Fraction of the signals sum and monitors sum.
                - "sum of fractions" : Sum of the signal and monitor fractions.

        """
        for scan in self.scans:
            if scan.monitor.size == 0:
                logger.info(
                    "No monitor data for scan %s. Setting aggregation mode to sum.",
                    scan.label,
                )
                mode = "sum"

        self._signal = np.zeros_like(self.x)
        if mode != "sum":
            self._monitor = np.zeros_like(self.x)

        for scan in self.scans:
            if mode in ("sum", "fraction of sums"):
                self._signal += np.nan_to_num(scan.signal, nan=0)
            elif mode in ("sum of fractions",):
                self._signal += np.nan_to_num(scan.signal, nan=0) / np.nan_to_num(
                    scan.monitor, nan=1
                )
            else:
                raise ValueError(f"Unknown aggregation mode {mode}.")

            # Aggregate monitor when mode is not "sum".
            if mode != "sum" and self._monitor.size > 0:
                self._monitor += np.nan_to_num(scan.monitor, nan=0)

        # Divide signal by monitor where monitor is not zero. If monitor is zero, the
        # signal is set to NaN.
        if mode == "fraction of sums":
            self._signal = np.where(
                self._monitor != 0, self._signal / self._monitor, np.nan
            )

        logger.info("The scans data was aggregated using the %s mode.", mode)

    def normalize(self, mode: str = "area") -> None:
        """
        Normalize the signal.

        Parameters
        ----------
        mode :
            Defines how the signal is normalized.

              - "area": Normalize using the absolute signal area calculated using the
                trapezoidal rule.
              - "maximum": Normalize using the absolute maximum intensity of the signal.

        Notes
        -----
        This will overwrite the original signal with the normalized one.
        """
        if self._signal.size == 0:
            self.aggregate()

        if mode == "area":
            self._signal = self._signal / np.abs(trapezoid(self._signal, self.x))
        elif mode == "maximum":
            self._signal = self._signal / np.abs(np.nanmax(self._signal))
        else:
            raise ValueError(f"Unknown normalization mode {mode}.")

        logger.info("The signal was normalized using the %s.", mode)

    def dead_time_correction(
        self,
        tau: Iterable[float],
        detection_time: float | npt.NDArray[np.float64] | None = None,
    ):
        """
        Perform a dead time correction using a non-paralyzable model.

        See the docstring of :meth:`.scans.Scan.dead_time_correction`.
        """
        for scan in self.scans:
            scan.dead_time_correction(tau, detection_time)

    def save(self, filename: str, delimiter: str = ","):
        """
        Save the current x and signal to file.

        Parameters
        ----------
        filename :
            Name of the output file.
        delimiter :
            Column delimiter in the output file.
        """
        if self.signal.size == 0:
            raise ValueError("The signal is not defined.")

        with open(filename, "w", encoding="utf-8") as fp:
            fp.write("# x signal\n")
            data = np.stack((self.x, self.signal), axis=1)
            np.savetxt(fp, data, delimiter=delimiter, fmt="%.6e %.6e")
            logger.info("The data was saved to %s.", filename)


class Xas(Measurement1D):
    """Class to represent a X-ray absorption measurement."""


class Xes(Measurement1D):
    """Class to represent a X-ray emission measurement."""


class Measurement2D(Measurement):
    """Base class for 2D measurements."""


class Rixs(Measurement2D):
    """Class to represent a resonant inelastic X-ray scattering measurement."""

    def __init__(self, sources: Source | list[Source]):
        super().__init__(sources=sources)
        self._y: npt.NDArray[np.float64] = np.array([])
        self._interpolator: Interpolator2D | None = None
        self.cuts = {}

    @property
    def x(self):
        if self._x.size == 0:
            self.process()
        return self._x

    @property
    def y(self):
        if self._y.size == 0:
            self.process()
        return self._y

    @property
    def signal(self):
        if self._signal.size == 0:
            self.process()
        return self._signal

    @property
    def interpolator(self):
        """The interpolator of the current plane."""
        if self._interpolator is None:
            self._interpolator = Interpolator2D(self.x, self.y, self.signal)
        return self._interpolator

    @property
    def acquisition_mode(self):
        """
        There are two ways to measure a RIXS plane:

        1. Step through a range of emission energies and scan the incoming
           (monochromator) energy for each step.
        2. Step through incoming (monochromator) energy and scan the emission energy.
        """
        if all(scan.y is not None and scan.y.size == 1 for scan in self.scans):
            mode = "absorption"
        else:
            mode = "emission"
        logger.debug("The RIXS plane was acquired in %s mode.", mode)
        return mode

    def reset(self, scans: float = True):
        """Reset the measurement."""
        super().reset(scans=scans)
        self._y = np.array([])
        self._interpolator = None

    def find_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Find outliers in the data.

        See the docstring of :meth:`.scans.Scan.find_outliers`.
        """
        for scan in self.scans:
            scan.find_outliers(method=method, **kwargs)

    def remove_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Remove outliers from the signal.

        See the docstring of :meth:`.scans.Scan.remove_outliers`.
        """
        logger.info("Removing outliers.")
        for scan in self.scans:
            scan.remove_outliers(method=method, **kwargs)
        self._signal = np.array([])

    def concentration_correction(
        self,
        indices: int | list[int] | None | npt.NDArray[np.int64] = None,
        scans: Scan | list[Scan] | Scans | None = None,
        paths: dict[str, str] | None = None,
    ) -> None:
        super().concentration_correction(indices, scans, paths)
        self._y = np.array([])
        self._interpolator = None

    def process(self):
        """Read and store the scans data."""
        acquisition_mode = self.acquisition_mode

        if acquisition_mode == "emission":
            raise NotImplementedError("The emission mode is not implemented yet.")

        x, y, signal = np.array([]), np.array([]), np.array([])

        if acquisition_mode == "absorption":
            for scan in self.scans:
                x = np.append(x, scan.x)
                y = np.append(y, scan.y * np.ones_like(scan.x))
                if scan.monitor.size == 0:
                    signal = np.append(signal, scan.signal)
                else:
                    signal = np.append(signal, scan.signal / scan.monitor)

            # Convert to energy transfer.
            y = x - y

        self._x, self._y, self._signal = x, y, signal

    def interpolate(self, xi: npt.NDArray[np.float64], yi: npt.NDArray[np.float64], /):
        """
        Interpolate the plane using the new axes.

        Parameters
        ----------
        xi :
            The new X-axis.
        yi :
            The new Y-axis.

        """
        x, y = np.meshgrid(xi, yi)
        x = xi.ravel()
        y = yi.ravel()
        points = np.stack((x, y), axis=-1)
        signal = self.interpolator(points)

        # Flatten arrays for storage.
        signal = signal.ravel()

        # Remove NaNs.
        mask = np.isfinite(signal)
        x = x[mask]
        y = y[mask]
        signal = signal[mask]

        # Assign the values.
        self._x, self._y, self._signal = x, y, signal

        # Update the interpolator.
        self.interpolator.update({"x": x, "y": y, "z": signal})

    def cut(
        self,
        mode: str = "CEE",
        energies: list[float] | None = None,
        npoints: int = 1024,
    ):
        """
        Calculate the cuts specified by the mode and energies.

        Parameters
        ----------
        mode : str
            Defines the way to cut the plane:

            - "CEE" - constant emission energy
            - "CIE" - constant incident energy
            - "CET" - constant energy transfer

        energies : list(float)
            Energies of the cuts.

        npoints : int
            Number of points for the cuts.

        """
        if energies is None:
            raise ValueError("The energies parameter must be defined.")

        mode = mode.upper()

        # Update the xc and yc arrays depending on the type of cut.
        for energy in energies:
            xc = np.linspace(self.x.min(), self.x.max(), npoints)
            yc = np.linspace(self.y.min(), self.y.max(), npoints)

            if mode == "CEE":
                yc = xc - np.ones_like(xc) * energy
            elif mode == "CIE":
                xc = np.ones_like(yc) * energy
            elif mode == "CET":
                yc = np.ones_like(xc) * energy
            else:
                raise ValueError(f"Unknown mode {mode}.")

            points = np.stack((xc, yc), axis=-1)
            signal = self.interpolator(points)

            if np.isnan(signal).all():
                logger.info("The %s cut at %s is empty.", mode, energy)
                continue

            # Remove NaNs.
            mask = np.isfinite(signal)
            xc = xc[mask]
            yc = yc[mask]
            signal = signal[mask]

            label = f"{mode.upper()}@{energy}"
            self.cuts[label] = (xc, yc, signal)
