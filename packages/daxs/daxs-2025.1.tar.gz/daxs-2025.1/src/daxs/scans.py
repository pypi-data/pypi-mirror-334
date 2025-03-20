"""The module provides classes for the representation of scans in measurements."""

from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    import matplotlib.axes
import numpy as np
import numpy.typing as npt

from daxs.config import Config
from daxs.filters import hampel
from daxs.utils import arrays

logger = logging.getLogger(__name__)

use_blissdata_api = Config().get("use_blissdata_api", False)
if use_blissdata_api:
    from blissdata.h5api.dynamic_hdf5 import File
else:
    from silx.io.h5py_utils import File


class Scan:
    def __init__(
        self,
        x: npt.NDArray[np.float64] | None = None,
        signal: npt.NDArray[np.float64] | None = None,
        *,
        data: dict[Any, Any] | None = None,
    ) -> None:
        """Define the base representation of scans in measurements.

        An scan can be initialized in two ways:

        1. Direct initialization - by passing the `x` and `signal` directly to
           the constructor, with optional additional data.

        2. Lazy initialization - by creating an empty scan and then setting values
           through properties, either all at once via the `data` property or
           individually `x`, `signal`, `monitor`, etc.

        Parameters
        ----------
        x :
            X-axis values (1D array).
        signal :
            Signal values (1D or 2D array). For a 2D array, the components must be
            stored as rows. A 1D array will be converted to a 2D array.
        data :
            Storage for the raw scan data and metadata.
        """
        self._data = {} if data is None else data

        # Initialize empty arrays.
        self._x = np.array([])
        self._y = np.array([])
        self._signal = np.array([])
        self._monitor = np.array([])

        # Array of indices used to reindex the data.
        self._indices: npt.NDArray[np.int32] = np.array([])

        # Initialize the outliers and medians arrays.
        self.outliers: npt.NDArray[np.bool_] = np.array([])
        self.medians: npt.NDArray[np.float64] = np.array([])

        self.filename: str | None = None
        self.index: int | None = None

        self.aggregation: str = "mean"

        # Set the data from the input parameters.
        self.x = x if x is not None else np.array([])
        self.signal = signal if signal is not None else np.array([])
        for attr in ("y", "monitor"):
            if attr in self._data:
                setattr(self, attr, self._data[attr])
        # Reindex the data using the indices array that sorts the X-axis values.
        self.reindex()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, a: npt.NDArray[np.float64]) -> None:
        """Set the X-axis values.

        Several cases are considered:

        1. The first assignment. In this case, the new values are simply stored.
        2. The new values are the same as the current ones. In this case, nothing has
           to be done.
        3. The limits of the new values are within the current values. In this case,
           the signal and monitor data are interpolated to the new X-axis values.
        4. The new values are outside the current values, but the two arrays have the
           same shape. In this case, the new values are assigned to the X-axis. It
           is useful when the X-axis changes to different units, e.g., angle to energy,
           which does not require interpolation.
        5. The new values are outside the current values and of different shapes. In
           this case, an error is raised.

        The x values are used as the independent variable for all scan data. When
        changing x values, dependent variables like signal and monitor may need to be
        interpolated to maintain correct data relationships.

        Parameters
        ----------
        a : npt.NDArray[np.float64]
            The new x-axis values to set.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the input is not a NumPy array.
        ValueError
            If the new values are outside the range of the current values and
            the arrays have different shapes.
        """
        if not isinstance(a, np.ndarray):
            raise TypeError("The X-axis values must be a Numpy array.")

        # First assignment case.
        if "x" not in self._data:
            self._data["x"] = a
            self._x = a.astype(np.float64)
            return

        # Normal case with existing data.
        a = np.sort(a, kind="stable")

        if np.array_equal(self._x, a):
            logger.debug("The new X-axis values are the same as the current ones.")
            return
        elif arrays.intersect(a, self._x).size > 0:
            self.interpolate(a)
            return
        elif self._x.size == a.size:
            logger.debug("Assigning the new X-axis values.")
            self._x = a.astype(np.float64)
            self._indices = np.array([])
            return
        else:
            raise ValueError("The new X-axis values are outside the current ones.")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, a: npt.NDArray[np.float64]) -> None:
        """Set the Y-axis values.

        Parameters
        ----------
        a :
            Y-axis values (1D array).
        """
        if not isinstance(a, np.ndarray):
            raise TypeError("The Y-axis values must be a Numpy array.")

        if "y" not in self._data:
            self._data["y"] = a

        self._y = a.astype(np.float64)

    @property
    def signal(self):
        if self.aggregation == "mean":
            return self._signal.mean(axis=0)
        else:
            raise ValueError(f"Unknown aggregation method: {self.aggregation}.")

    @signal.setter
    def signal(self, a: npt.NDArray[np.float64]) -> None:
        """Set the signal values.

        Parameters
        ----------
        a :
            Signal values (1D or 2D array). For a 2D array, the components must be
            stored as rows. A 1D array will be converted to a 2D array.
        """
        if not isinstance(a, np.ndarray):
            raise TypeError("The signal values must be a Numpy array.")

        if a.ndim not in (1, 2):
            raise ValueError("The signal must be a 1D or a 2D array.")

        # Check if signal matches current x dimension.
        if self._x.size > 0 and a.size > 0 and self._x.size != a.shape[-1]:
            raise ValueError(
                f"The signal size ({a.shape[-1]}) must match the "
                f"X-axis size ({self._x.size})."
            )

        if "signal" not in self._data:
            self._data["signal"] = a

        self._signal = a.astype(np.float64)

        # Convert 1D signal to 2D for consistent internal representation.
        if self._signal.ndim == 1:
            self._signal = self._signal[np.newaxis, :]

    @property
    def monitor(self):
        return self._monitor

    @monitor.setter
    def monitor(self, a: npt.NDArray[np.float64]) -> None:
        """Set the monitor values.

        Parameters
        ----------
        a :
            Monitor values (1D array).
        """
        if not isinstance(a, np.ndarray):
            raise TypeError("The monitor values must be a Numpy array.")

        # Check if monitor size matches current x dimension.
        if self._x.size > 0 and a.size > 0 and a.size != self._x.size:
            raise ValueError(
                f"The monitor size ({a.size}) must match the "
                "X-axis size ({self._x.size})."
            )

        if "monitor" not in self._data:
            self._data["monitor"] = a

        self._monitor = a.astype(np.float64)

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, a: npt.NDArray[np.int32]) -> None:
        """Set the indices array.

        Parameters
        ----------
        a :
            Indices array (1D array).
        """
        if not isinstance(a, np.ndarray):
            raise TypeError("The indices must be a Numpy array.")

        if a.shape != self._x.shape:
            raise ValueError("The indices and X-axis arrays must have the same shape.")

        self._indices = a.astype(np.int32)
        self.reindex()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict[Any, Any]) -> None:
        """Set the data dictionary."""
        if not isinstance(data, dict):
            raise TypeError("The data must be a dictionary.")
        self._data = data
        self.reset()

    @property
    def label(self) -> str:
        return f"{self.filename}/{self.index}"

    def reset(self) -> None:
        """Reset the scan data to the original values stored internally."""
        try:
            self._x = self._data["x"].astype(np.float64)
        except KeyError as e:
            raise KeyError("The data dictionary does not contain X-axis values.") from e

        try:
            self._y = self._data["y"].astype(np.float64)
        except KeyError:
            logger.debug("The data dictionary does not contain Y-axis values.")

        try:
            self._signal = self._data["signal"].astype(np.float64)
        except KeyError as e:
            raise KeyError("The data dictionary does not contain signal values.") from e

        # The stored signal may be a 1D array, so we need to convert it to a 2D array.
        if self._signal.ndim == 1:
            self._signal = self._signal[np.newaxis, :]

        try:
            self._monitor = self._data["monitor"].astype(np.float64)
        except KeyError:
            logger.debug("The data dictionary does not contain monitor values.")

        self._indices = np.array([])
        self.outliers, self.medians = np.array([]), np.array([])

        # Only reindex if we have valid data.
        if self._x.size > 0 and self._signal.size > 0:
            self.reindex()
        else:
            logger.warning(
                f"The x and signal arrays are empty for scan {self.label}. "
                "Skipping reindexing."
            )

    def reindex(self):
        """Reindex the scan data."""
        if self._x.size == 0:
            return
        if self._indices.size == 0:
            self._indices = np.argsort(self._x, kind="stable")
        self._x = self._x[self._indices]
        self._signal = self._signal[:, self._indices]
        if self._monitor.size != 0:
            self._monitor = self._monitor[self._indices]

    def read_data_at_paths(
        self, data_paths: str | list[str]
    ) -> npt.NDArray[np.float64]:
        """Read and store the data from the file."""
        if self.filename is None:
            raise ValueError("The filename from where to read the data must be set.")
        if self.index is None:
            raise ValueError("The scan index from where to read the data must be set.")

        data_paths = [data_paths] if isinstance(data_paths, str) else data_paths

        kwargs: dict[Any, Any] = {}
        if use_blissdata_api:
            kwargs["retry_timeout"] = Config().get("dynamic_hdf5_retry_timeout")

        data: list[Any] = []
        with File(self.filename, **kwargs) as fh:
            for data_path in data_paths:
                full_data_path = f"{self.index}{data_path}"

                try:
                    data_at_path = fh[full_data_path][()]  # type: ignore
                except KeyError as e:
                    raise KeyError(f"Unable to access {full_data_path}.") from e
                except TypeError as e:
                    raise TypeError(
                        f"Unable to read data from {full_data_path}."
                    ) from e

                try:
                    data_at_path = np.asarray(data_at_path)  # type: ignore
                except ValueError as e:
                    raise ValueError(
                        f"Unable to convert data from {full_data_path} "
                        "to a Numpy array."
                    ) from e

                if data_at_path.size == 0:
                    raise ValueError(f"Data from {full_data_path} is empty.")

                data.append(data_at_path)

        # Return the element of the array if it has only one element.
        if len(data) == 1:
            [data] = data

        return np.array(data)

    def find_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Find outliers in the signal.

        See the docstring in the :mod:`daxs.filters`.
        """
        if method == "hampel":
            self.outliers, self.medians = hampel(self._signal, axis=1, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}.")

    def remove_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Remove outliers from the signal.

        See the docstring of :meth:`daxs.scans.Scan.find_outliers`.
        """
        if self.outliers.size == 0 or self.medians.size == 0:
            self.find_outliers(method=method, **kwargs)

        if self.outliers.size > 0 and self.medians.size > 0:
            self._signal = np.where(self.outliers, self.medians, self._signal)
        else:
            logger.info("No outliers found for scan %s.", self.label)

    def dead_time_correction(
        self,
        tau: Iterable[float],
        detection_time: float | npt.NDArray[np.float64] | None = None,
    ):
        """
        Perform a dead time correction using a non-paralyzable model.

        Parameters
        ----------
        tau :
            The detector dead time in seconds.
        detection_time :
            The time spent on a point of the scan in seconds.

        """
        if detection_time is None:
            try:
                detection_time = copy.deepcopy(self._data["detection_time"])
            except KeyError:
                raise ValueError(
                    "Either the detection time parameter or `detection_time`"
                    " data path must be set."
                )
        else:
            detection_time = np.ones_like(self.signal) * detection_time

        detection_time = np.asarray(detection_time)

        if np.any(detection_time == 0):
            raise ValueError("The detection time has zero values.")

        tau = np.array(tau)
        if self._signal.shape[0] != tau.shape[0]:
            raise ValueError(
                "Each signal data path must have a detector dead time (tau) value."
            )

        norm = 1 - ((self._signal / detection_time).T * tau).T
        if np.any(norm == 0):
            raise ValueError("The normalization has zero values.")

        self._signal = self._signal / norm

    # TODO: Extract the interpolation logic to a separate class.
    def interpolate(self, a: npt.NDArray[np.float64]):
        """
        Interpolate the signal and possibly the monitor data to the new X-axis values.

        Parameters
        ----------
        a :
            Array used to interpolate the signal and monitor.

        """
        if a.size == 0:
            raise ValueError("The new X-axis values can not be empty.")

        if self._signal.size == 0:
            raise ValueError("The signal values must not be empty.")

        logger.debug(
            "Interpolating the signal and monitor data for scan %s.", self.label
        )

        # The interpolated signal is probably going to have a different size,
        # so we can't change the values in-place, and a new array needs to be
        # initialized.
        signal = np.zeros((self._signal.shape[0], a.size))

        # Interpolate the signal from each counter individually.
        for i, _ in enumerate(self._signal):
            signal[i, :] = np.interp(
                a, self._x, self._signal[i, :], left=np.nan, right=np.nan
            )

        # Interpolate the monitor if present.
        if self._monitor.size > 0:
            self._monitor = np.interp(
                a, self._x, self._monitor, left=np.nan, right=np.nan
            )

        self._x = a
        self._signal = signal
        self._indices = np.array([])

    def divide_by_scalars(
        self, signal: int | float, monitor: int | float | None = None
    ) -> Scan:
        """Divide the scan by scalar values."""
        self._signal /= signal
        if monitor is not None:
            self._monitor /= monitor
        return self

    def divide_by_scan(self, other: Scan) -> Scan:
        """Divide the scan by another scan."""
        if not isinstance(other, Scan):
            raise TypeError("The divisor must be a scan.")

        try:
            self._signal /= np.nan_to_num(other._signal, nan=1)
        except ValueError as e:
            raise ValueError(
                "The signal arrays of the two scans must have the same shape."
            ) from e

        # Check for empty or all-zero divisors.
        if other._signal.size == 0:
            raise ValueError("Cannot divide an empty signal.")
        if np.all(other._signal == 0):
            raise ValueError("Cannot divide by signal with all zero values.")

        if self._monitor.size > 0 and other._monitor.size > 0:
            if np.all(other._monitor == 0):
                logger.warning(
                    "Monitor values are all zero. This may result in invalid data."
                )
            try:
                self._monitor /= np.nan_to_num(other._monitor, nan=1)
            except ValueError as e:
                raise ValueError(
                    "The monitor arrays of the two scans must have the same shape."
                ) from e

        return self

    def __truediv__(self, other: Scan) -> Scan:
        """Divide the scan by another scan."""
        return self.divide_by_scan(other)

    def plot(self, ax: matplotlib.axes.Axes, shift: float = 0.0):
        """
        Plot the scan data and outliers if available.

        Parameters
        ----------
        ax :
            The axes to plot the scan data on.
        shift :
            Shift the signal by the given value.

        """
        shift = float(np.mean(self._signal))
        for i, _ in enumerate(self._signal):
            ax.plot(self.x, self._signal[i, :] + i * shift, label=f"{i}")
            if self.outliers.size > 0:
                indices = self.outliers[i, :]
                ax.plot(self.x[indices], self._signal[i, :][indices] + i * shift, "k.")
            ax.legend()

    def __str__(self):
        return self.label


class Scans:
    """A collection of scans."""

    def __init__(self, scans: Scan | list[Scan] | None = None) -> None:
        """Initialize the collection of scans."""
        if scans is None:
            self.scans = []
        elif isinstance(scans, list):
            self.scans = scans
        else:
            self.scans = [scans]

    def check_sizes(self) -> None:
        """Sanity check for the number of points in the scans."""
        sizes = [scan.x.size for scan in self.scans]
        mean = np.mean(sizes)
        std = np.std(sizes)

        if any(abs(size - mean) > std for size in sizes):
            logger.warning(
                "The number of points in the selected scans have a "
                "large spread (mean = %.2f, standard deviation: %.2f).",
                mean,
                std,
            )

    # TODO: Extract the common axis logic to a utility function.
    def get_common_axis(
        self, label: str = "x", mode: str = "intersection"
    ) -> npt.NDArray[np.float64]:
        """Return the common axis for the scans."""
        if not self.scans:
            raise ValueError("There are no scans available.")

        def step(axis: npt.NDArray[np.float64]) -> float:
            return np.abs((axis[0] - axis[-1]) / (axis.size - 1))

        # If there is a single scan, use its axis as the common axis.
        if len(self.scans) == 1:
            [axis] = self.scans
            return getattr(axis, label)

        axes = sorted([getattr(scan, label) for scan in self.scans], key=np.min)

        # Initialize the common axis as the first axis.
        common_axis = axes[0]
        for i, axis in enumerate(axes):
            message = (
                f"{label.upper()}-axis parameters for scan {self.scans[i].label}: "
                f"start = {axis[0]:.8f}, stop = {axis[-1]:.8f}, "
                f"size = {axis.size:d}, step = {step(axis):.8f}."
            )
            logger.debug(message)

            if np.array_equal(common_axis, axis):
                continue

            common_axis = arrays.merge(common_axis, axis, mode=mode)

            if common_axis.size == 0 and mode == "intersection":
                message = (
                    f"The common {label.upper()}-axis is empty after merging scan "
                    f"{self.scans[i].label}. "
                    "Switching to union mode for the common axis search."
                )
                logger.warning(message)
                return self.get_common_axis(label, mode="union")

        message = (
            f"Common {label.upper()}-axis parameters using {mode} mode: "
            f"start = {common_axis[0]:.8f}, stop = {common_axis[-1]:.8f}, "
            f"size = {common_axis.size:d}, step = {step(common_axis):.8f}"
        )
        logger.info(message)

        return common_axis

    def reset(self) -> None:
        """Reset the scans to their original values."""
        for scan in self.scans:
            scan.reset()

    def extend(self, scans: Scans) -> None:
        """Extend the collection of scans."""
        self.scans.extend(scans)

    def __len__(self) -> int:
        """Return the number of scans in the collection."""
        return len(self.scans)

    def __iter__(self):
        """Iterate over the scans."""
        return iter(self.scans)

    def __getitem__(self, index: int) -> Scan:
        """Return the scan at the given index."""
        return self.scans[index]

    def __str__(self):
        """Return a string representation of the collection."""
        return "\n".join([str(scan) for scan in self.scans])

    def remove(self, item: Scan) -> None:
        """Remove the scan at the given index."""
        self.scans.remove(item)

    def append(self, item: Scan) -> None:
        """Append a scan to the collection."""
        self.scans.append(item)
