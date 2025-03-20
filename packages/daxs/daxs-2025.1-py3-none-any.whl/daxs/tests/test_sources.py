from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from pathlib import Path

import h5py
import numpy as np
import pytest

from daxs.sources import BlissPath, Hdf5Source, Selection


# TODO: Use collection instead of sample.
def test_bliss_path():
    bliss_path = BlissPath(
        root="/data/visitor",
        proposal="blc1234",
        beamline="id00",
        session="20240101",
        sample="sample_1",
        dataset="xanes_0001",
    )
    assert bliss_path.session == "20240101"
    assert bliss_path.filename == "sample_1_xanes_0001.h5"
    assert bliss_path.path == (
        "/data/visitor/blc1234/id00/20240101/RAW_DATA"
        "/sample_1/sample_1_xanes_0001/sample_1_xanes_0001.h5"
    )
    bliss_path.sample = "sample_2"
    assert bliss_path.path == (
        "/data/visitor/blc1234/id00/20240101/RAW_DATA"
        "/sample_2/sample_2_xanes_0001/sample_2_xanes_0001.h5"
    )

    path = (
        "/data/visitor/blc1234/id00/20240101/RAW_DATA"
        "/sample_1/sample_1_xanes_0001/sample_1_xanes_0001.h5"
    )
    bliss_path = BlissPath.from_path(path)
    assert bliss_path.path == path


def test_selection_invalid():
    with pytest.raises(ValueError):
        list(Selection("1-3"))
    with pytest.raises(ValueError):
        list(Selection([1, 2, "fscan"]))  # type: ignore


@pytest.mark.parametrize(
    "items, normalized_items",
    (
        (1, [1]),
        ([1, 2, 3], [1, 2, 3]),
        (np.array([1, 2, 3.0]), [1, 2, 3]),
    ),
)
def test_selection(items: int | str, normalized_items: list[int | str]):
    assert list(Selection(items)) == normalized_items


@pytest.mark.parametrize(
    "included_scan_ids, excluded_scan_ids, selected_scan_ids",
    (
        ([1, 2, 3, 4], None, [1, 2, 3, 4]),
        ([1, 2, 3], np.array([1, 2, 3]), []),
        (np.array([1, 2, 3]), None, [1, 2, 3]),
    ),
)
def test_hdf5_source_selected_scans(
    mock_hdf5_path: str,
    included_scan_ids: Any,
    excluded_scan_ids: Any,
    selected_scan_ids: list[int],
):
    source = Hdf5Source(
        mock_hdf5_path, included_scan_ids, excluded_scan_ids, data_mappings={}
    )
    assert source.selected_scan_ids == selected_scan_ids


@pytest.fixture
def mock_hdf5_path(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    path = tmp_path_factory.mktemp("files") / "mock_hdf5_filename.h5"
    with h5py.File(path, "w") as f:
        f.create_dataset("1.1/instrument/name", data="detector")
        f.create_dataset("2.1/measurement/x", data=[1, 2, 3])
        f.create_dataset("2.1/measurement/signal", data=[2, 2, 2])
        f.create_dataset("2.1/instrument/name", data="detector")
        f.create_dataset("3.1/measurement/x", data=[10, 20, 30])
        f.create_dataset("3.1/measurement/signal", data=[4.1, 5.1, 6.1])
        f.create_dataset("3.1/measurement/monitor", data=[7.0, 8.0, 9.0])
        f.create_dataset("3.1/measurement/sec", data=[1, 1, 1])
    yield path
    os.remove(path)


def test_hdf5_source_scans(mock_hdf5_path: str):
    data_mappings = {}
    source = Hdf5Source(mock_hdf5_path, 1, None, data_mappings)
    with pytest.raises(ValueError):
        assert source.scans

    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(mock_hdf5_path, 1, None, data_mappings)
    with pytest.raises(KeyError):
        assert source.scans

    data_mappings["name"] = ".1/instrument/name"
    source = Hdf5Source(mock_hdf5_path, 2, None, data_mappings)
    assert source.scans[0].data["name"] == b"detector"
    data_mappings.pop("name")

    data_mappings["monitor"] = ".1/measurement/monitor"
    source = Hdf5Source(mock_hdf5_path, 3, None, data_mappings)
    assert np.all(source.scans[0].monitor == np.array([7.0, 8.0, 9.0]))
    data_mappings.pop("monitor")

    data_mappings["detection_time"] = ".1/measurement/detection_time"
    source = Hdf5Source(mock_hdf5_path, 3, None, data_mappings)
    with pytest.raises(KeyError):
        assert source.scans

    data_mappings["detection_time"] = ".1/measurement/sec"
    source = Hdf5Source(mock_hdf5_path, 3, None, data_mappings)
    assert np.all(source.scans[0].data["detection_time"] == np.array([1.0, 1.0, 1.0]))
    data_mappings.pop("detection_time")

    source = Hdf5Source(mock_hdf5_path, [2, 3], None, data_mappings)
    scans = source.scans
    assert np.all(scans[0].x == np.array([1, 2, 3]))
    assert np.all(scans[1].x == np.array([10, 20, 30]))

    source = Hdf5Source(mock_hdf5_path, [9], None, data_mappings)
    with pytest.raises(KeyError):
        source.scans
