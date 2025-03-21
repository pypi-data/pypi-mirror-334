from pathlib import Path
import pytest
from ewoksorange.tests.utils import execute_task

from ewoks3dxrd.tasks.segment_frame import SegmentFrame


def test_segment_frame(inp_config):

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

    inputs = {
        "folder_config": sample_folder_config,
        "segmenter_algo_params": segmenter_config,
        "correction_files": file_cor_config,
    }
    task = SegmentFrame(inputs=inputs)
    task.execute()
    outputs = task.outputs

    raw_image = outputs["raw_image"]
    bg_corrected_image = outputs["bg_corrected_image"]
    found_peaks = outputs["found_peaks"]
    assert raw_image is not None
    assert bg_corrected_image is not None
    assert found_peaks is not None
    assert len(found_peaks) == 2
    assert len(found_peaks[0]) == 76


def test_wrong_threshold(inp_config):
    segmenter_config = {
        "threshold": "not_a_valid_threshold",
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

    with pytest.raises(RuntimeError) as exc_info:
        execute_task(
            SegmentFrame,
            inputs={
                "folder_config": sample_folder_config,
                "segmenter_algo_params": segmenter_config,
                "correction_files": file_cor_config,
            },
        )
    assert "Input should be a valid integer" in str(exc_info.value.__cause__)
