from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from pathlib import Path

import h5py
import numpy as np
import pytest

from daxs.measurements import (
    ConcentrationCorrectionError,
    Measurement,
    Measurement1D,
    Rixs,
    SimpleConcentrationCorrector,
)
from daxs.scans import Scan, Scans
from daxs.sources import Hdf5Source
from daxs.utils import resources


def test_simple_concentration_correction_mock():
    # The same number of scans and points in the concentration correction scan.
    conc_corr_scan = Scan(None, np.array([0.5, 1.0]))
    corrector = SimpleConcentrationCorrector(conc_corr_scan)
    scans = [
        Scan(None, np.array([1.0, 2.0, 3.0])),
        Scan(None, np.array([4.0, 5.0, 6.0])),
    ]
    scans = Scans(scans)
    corrector.apply(scans)
    assert np.allclose(scans[0].signal, np.array([2, 4, 6]))
    assert np.allclose(scans[1].signal, np.array([4, 5, 6]))

    scans[0].monitor = np.array([10, 20, 30])
    conc_corr_scan.monitor = np.array([100, 200])
    corrector.apply(scans)
    assert np.allclose(scans[0].monitor, np.array([0.1, 0.2, 0.3]))

    # Different number of scans and points in the concentration correction scan.
    # The concentration correction scan has the same number of points as the scans.
    scans.reset()
    conc_corr_scan = Scan(None, np.array([0.5, 1.0, 2.0]))
    corrector = SimpleConcentrationCorrector(conc_corr_scan)
    corrector.apply(scans)
    assert np.allclose(scans[0].signal, np.array([2, 2, 1.5]))
    assert np.allclose(scans[1].signal, np.array([8, 5, 3]))

    # The number of scans and concentration correction scans is the same.
    scans.reset()
    conc_corr_scans = [
        Scan(None, np.array([0.5, 1.0, 2.0])),
        Scan(None, np.array([1.0, 2.0, 3.0])),
    ]
    conc_corr_scans = Scans(conc_corr_scans)
    corrector = SimpleConcentrationCorrector(conc_corr_scans)
    corrector.apply(scans)
    assert np.allclose(scans[0].signal, np.array([2, 2, 1.5]))
    assert np.allclose(scans[1].signal, np.array([4, 2.5, 2]))


@pytest.fixture
def mock_hdf5_path(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    path = tmp_path_factory.mktemp("files") / "tmp.h5"
    with h5py.File(path, "w") as fh:
        for i in range(1, 4):
            fh.create_dataset(f"{i}.1/measurement/x", data=[i, i + 1, i + 2])
            fh.create_dataset(f"{i}.1/measurement/signal", data=[i, i * 2, i * 3])
    yield path
    os.remove(path)


def test_measurement_init(mock_hdf5_path: str):
    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(mock_hdf5_path, None, None, data_mappings)

    with pytest.raises(ValueError):
        measurement = Measurement(source)
        _ = measurement.scans

    source = Hdf5Source(mock_hdf5_path, 1, None, data_mappings)
    measurement = Measurement(source)
    assert np.allclose(measurement.scans[0].signal, np.array([1, 2, 3]))

    source = Hdf5Source(mock_hdf5_path, [1, 2], None, data_mappings)
    measurement = Measurement(source)
    assert np.allclose(measurement.scans[1].x, np.array([2, 3, 4]))
    assert np.allclose(measurement.scans[1].signal, np.array([2, 4, 6]))


def test_measurement_remove_scans(mock_hdf5_path: str):
    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(mock_hdf5_path, [1, 2, 3], None, data_mappings)
    measurement = Measurement(source)

    indices = [1, 2, 3]
    measurement.remove_scans(indices)
    assert len(measurement.scans) == 0


@pytest.fixture()
def hdf5_path() -> str:
    return resources.getfile("Pd_foil_La_XANES.h5")


@pytest.fixture()
def data_mappings():
    return {
        "x": ".1/measurement/hdh_angle",
        "signal": [".1/measurement/g09", ".1/measurement/g14"],
    }


def test_measurement1d_properties(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [3, 4, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert measurement.x[-1] == pytest.approx(38.72936736)
    assert measurement.signal[-1] == pytest.approx(21.1642857)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [3, 4, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert measurement.monitor[-1] == pytest.approx(167717.885714)

    measurement.process(normalization="area")
    assert measurement.signal[-1] == pytest.approx(0.0012821686)

    measurement.x = np.append(measurement.x, 39.0)
    assert np.isnan(measurement.signal[-1])


def test_measurement1d_aggregate(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert np.all(measurement.x == measurement.scans[0].x)

    measurement.aggregate()
    assert np.all(measurement.signal == measurement.scans[0].signal)

    assert np.all(measurement.signal == measurement.scans[0].signal)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    measurement.aggregate()
    assert measurement.signal[-1] == pytest.approx(0.0001546175)

    source = Hdf5Source(hdf5_path, [3, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    measurement.aggregate(mode="fraction of sums")
    assert measurement.signal[-1] == pytest.approx(0.0001306488)

    measurement.reset()
    measurement.aggregate(mode="sum of fractions")
    assert measurement.signal[-1] == pytest.approx(0.0002612987)

    with pytest.raises(ValueError):
        measurement.aggregate(mode="wrong")


def test_measurement1d_normalize(hdf5_path: str, data_mappings: dict[str, Any]):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)

    with pytest.raises(ValueError):
        measurement.normalize(mode="wrong")

    measurement.normalize(mode="area")
    assert measurement.signal[-1] == pytest.approx(0.0015740913)

    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)

    measurement.reset()
    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)


def test_measurement1d_outliers(hdf5_path: str, data_mappings: dict[str, Any]):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)

    measurement.find_outliers(method="hampel", threshold=2.0)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [28, 60])

    measurement.reset()
    measurement.remove_outliers(method="hampel", threshold=3.5)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [123, 284])


def test_measurement1d_dead_time_correction(
    hdf5_path: str, data_mappings: dict[str, Any]
):
    data_mappings.update({"detection_time": ".1/measurement/sec"})
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    with pytest.raises(TypeError):
        measurement.dead_time_correction()  # type: ignore
    measurement.dead_time_correction(tau=[0.1, 0.1])


def test_measurement1d_save(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    with pytest.raises(TypeError):
        measurement.save()  # type: ignore
    filename = "test.dat"
    measurement.save(filename)
    assert os.path.isfile(filename)
    os.remove(filename)


@pytest.mark.parametrize(
    "scan_ids, conc_corr_ids, expected",
    (
        ([4], [5], [0.0750053, 0.06380908]),
        ([4, 10], [5, 11], [0.07468005, 0.06404491]),
        ([4], [6], ConcentrationCorrectionError),
        ([4, 10], [5, 11, 12], ConcentrationCorrectionError),
    ),
)
def test_simple_concentration_correction_equal_number_of_scans(
    scan_ids: list[int], conc_corr_ids: list[int], expected: Any
):
    hdf5_path: str = resources.getfile("A1_Kb_XES.h5")
    data_mappings = {
        "x": ".1/measurement/xes_en",
        "signal": ".1/measurement/det_dtc_apd",
        "monitor": ".1/measurement/I02",
    }

    source = Hdf5Source(hdf5_path, scan_ids, data_mappings=data_mappings)
    measurement = Measurement1D(source)
    if isinstance(expected, list):
        measurement.concentration_correction(conc_corr_ids)
        assert measurement.signal[-2:] == pytest.approx(expected)
    else:
        with pytest.raises(expected):
            measurement.concentration_correction(conc_corr_ids)


def test_simple_concentration_correction_equal_number_of_scans_and_points():
    hdf5_path = resources.getfile("Fe2O3_Ka1Ka2_RIXS.h5")
    data_mappings = {
        "x": ".1/measurement/zaptime",
        "y": ".1/instrument/positioners/xes_en",
        "signal": [".1/measurement/det_dtc_apd"],
        "monitor": ".1/measurement/I02",
    }
    source = Hdf5Source(hdf5_path, list(range(4, 225)), data_mappings=data_mappings)
    measurement = Rixs(source)
    measurement.concentration_correction([225])
    assert measurement.scans[0].signal[-1] == pytest.approx(0.01887687)
    assert measurement.scans[-1].monitor[0] == pytest.approx(0.24412638)
    assert measurement.signal.mean() == pytest.approx(0.02197076489)
