import os
from pathlib import Path

import h5py
import pytest
from ewoksorange.canvas.handler import OrangeCanvasHandler
from ewoksorange.tests.conftest import qtapp  # noqa F401
from ImageD11.grain import read_grain_file


@pytest.fixture(scope="session")
def ewoks_orange_canvas(qtapp):  # noqa F811
    with OrangeCanvasHandler() as handler:
        yield handler


@pytest.fixture
def inp_config(tmp_path):
    scan_folder = (
        "/data/projects/id03_3dxrd/expt/RAW_DATA/FeAu_0p5_tR/FeAu_0p5_tR_ff1/scan0001"
    )

    if not os.path.exists(scan_folder):
        raise FileNotFoundError(
            f"""
            Could not find {scan_folder}.
            Before running this test, be sure to have a link to /data/projects at /data/:
             - mkdir -p /data/projects/id03_3dxrd
             - ln -s /gpfs/.../data/projects /data
            Sudo rights might be needed.
            """
        )

    return {
        "detector": "frelon3",
        "omega_motor": "diffrz",
        "dty_motor": "diffty",
        "bg_file": None,
        "mask_file": "/data/projects/id03_3dxrd/expt/PROCESSED_DATA/mask.edf",
        "spline_file": "/data/projects/id03_3dxrd/expt/PROCESSED_DATA/frelon36.spline",
        "e2dx_file": None,
        "e2dy_file": None,
        "scan_folder": scan_folder,
        "analyse_folder": os.path.join(tmp_path, "test_my_task"),
        "stateful_imageD11_file": None,
    }


def assert_indexing_results(indexing_task_outputs):
    ubi_file_path = indexing_task_outputs["grain_ubi_file"]
    assert Path(ubi_file_path).exists()
    h5_file_path = indexing_task_outputs["grain_nexus_file"]
    assert Path(h5_file_path).exists()
    with h5py.File(h5_file_path, "r") as f:
        assert f["entry/indexed_grains/grains/UBI"][()].shape == (59, 3, 3)
        assert f["entry/indexed_grains/grains/translation"][()].shape == (59, 3)


def assert_grain_map_results(grain_map_task_outputs):
    ascii_grains_file = grain_map_task_outputs["ascii_grain_map_file"]
    assert Path(ascii_grains_file).exists()
    list_grains = read_grain_file(ascii_grains_file)
    assert len(list_grains) == 52
