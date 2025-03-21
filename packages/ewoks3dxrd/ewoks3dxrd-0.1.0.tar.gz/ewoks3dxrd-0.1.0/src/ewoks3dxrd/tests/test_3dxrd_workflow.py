import sys

if sys.version_info >= (3, 9):
    from importlib.resources import files as resource_files
else:
    from importlib_resources import files as resource_files

from pathlib import Path

import numpy as np
from ewokscore import execute_graph
from ImageD11 import columnfile as PeakColumnFile

from orangecontrib.ewoks3dxrd import tutorials

from .conftest import assert_indexing_results, assert_grain_map_results


def test_segmentation_3dpeaks_workflow(inp_config):
    # if you change this config setting or default inp_config,
    # assertion statement assert len(found_peaks[0]) == 76 and
    # and len(peaks_position[0]) == 31682 and
    # assert cf.nrows == 7662 will fail

    # if you change this config setting,
    # assertion statement assert len(found_peaks[0]) == 76 will fail
    segmenter_config = {
        "threshold": 70,
        "smooth_sigma": 1.0,
        "bgc": 0.9,
        "min_px": 3,
        "offset_threshold": 100,
        "ratio_threshold": 150,
    }

    file_cor_config = {
        "bg_file": inp_config.get("bg_file"),
        "mask_file": inp_config.get("mask_file"),
        "flat_file": None,
        "dark_file": None,
    }

    scan_folder = Path(inp_config.get("scan_folder"))
    sample_folder_config = {
        "detector": "frelon3",
        "omega_motor": "diffrz",
        "scan_folder": str(scan_folder),
        "analyse_folder": inp_config.get("analyse_folder"),
    }

    inputs = [
        {
            "name": "folder_config",
            "value": sample_folder_config,
            "id": "segScan",
        },
        {
            "name": "segmenter_algo_params",
            "value": segmenter_config,
            "id": "segScan",
        },
        {
            "name": "correction_files",
            "value": file_cor_config,
            "id": "segScan",
        },
        {
            "name": "correction_files",
            "value": inp_config["spline_file"],
            "id": "DetCor",
        },
        {
            "name": "geometry_par_file",
            "value": "/data/projects/id03_3dxrd/expt/PROCESSED_DATA/geometry_tdxrd.par",
            "id": "GeoUp",
        },
        {
            "name": "lattice_par_file",
            "value": "/data/projects/id03_3dxrd/expt/PROCESSED_DATA/Fe.par",
            "id": "LatFilt",
        },
        {
            "name": "lattice_par_file",
            "value": "/data/projects/id03_3dxrd/expt/PROCESSED_DATA/Fe.par",
            "id": "AllLatFilt",
        },
        {
            "name": "reciprocal_dist_max",
            "value": 1.01,
            "id": "LatFilt",
        },
        {
            "name": "reciprocal_dist_tol",
            "value": 0.01,
            "id": "LatFilt",
        },
        {
            "name": "reciprocal_dist_tol",
            "value": 0.01,
            "id": "AllLatFilt",
        },
        {
            "name": "intensity_frac",
            "value": 0.9837,
            "id": "IntFilt",
        },
        {
            "name": "intensity_frac",
            "value": 0.9837,
            "id": "AllIntFilt",
        },
        {
            "name": "reciprocal_dist_tol",
            "value": 0.05,
            "id": "Indexer",
        },
        {
            "name": "gen_rings_from_idx",
            "value": (0, 1),
            "id": "Indexer",
        },
        {
            "name": "score_rings_from_idx",
            "value": (0, 1, 2, 3),
            "id": "Indexer",
        },
        {
            "name": "hkl_tols",
            "value": (0.01, 0.02, 0.03, 0.04),
            "id": "Indexer",
        },
        {
            "name": "min_pks_frac",
            "value": (0.9, 0.75),
            "id": "Indexer",
        },
        {
            "name": "cosine_tol",
            "value": np.cos(np.radians(90 - 0.25)),
            "id": "Indexer",
        },
        {
            "name": "max_grains",
            "value": 1000,
            "id": "Indexer",
        },
        {
            "name": "lattice_name",
            "value": "Fe",
            "id": "Indexer",
        },
        {
            "name": "hkl_tols",
            "value": (0.05, 0.025, 0.01),
            "id": "GrainMap",
        },
        {
            "name": "minpks",
            "value": 120,
            "id": "GrainMap",
        },
        {
            "name": "lattice_name",
            "value": "Fe",
            "id": "GrainMap",
        },
    ]
    workflow_file = resource_files(tutorials).joinpath("3dxrd_workflow.json")

    outputs = execute_graph(
        str(workflow_file), inputs=inputs, outputs=[{"all": True}], merge_outputs=False
    )
    assert outputs is not None
    detector_spatial_file_path = outputs["DetCor"][
        "detector_spatial_corrected_3d_peaks_file"
    ]
    assert Path(detector_spatial_file_path).exists()
    detector_spatial_corrected_columnfile = PeakColumnFile.columnfile(
        filename=detector_spatial_file_path
    )
    peak_x_position = detector_spatial_corrected_columnfile.f_raw
    assert len(peak_x_position) == 31682
    filtered_h5_col_file = outputs["LatFilt"]["filtered_h5_col_file"]
    filtered_flt_col_file = outputs["LatFilt"]["filtered_flt_col_file"]
    lattice_par_file = outputs["LatFilt"]["copied_lattice_par_file"]

    assert Path(filtered_h5_col_file).exists()
    assert Path(filtered_flt_col_file).exists()
    assert Path(lattice_par_file).exists()

    int_flt_h5_file = outputs["IntFilt"]["Ifilt_h5_col_file"]
    int_flt_flt_file = outputs["IntFilt"]["Ifilt_flt_col_file"]
    assert Path(int_flt_h5_file).exists()
    assert Path(int_flt_flt_file).exists()
    cf = PeakColumnFile.columnfile(filename=int_flt_h5_file)
    assert cf.nrows == 7662

    assert_indexing_results(outputs["Indexer"])

    assert_grain_map_results(outputs["GrainMap"])
