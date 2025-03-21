from ewoks3dxrd.tasks.make_grain_map import MakeGrainMap

from .conftest import assert_grain_map_results


def test_map_grains():
    inputs = {
        "hkl_tols": (0.05, 0.025, 0.01),
        "minpks": 120,
        "lattice_name": "Fe",
        "folder_file_config": {
            "omega_motor": "diffrz",
            "scan_folder": "/data/projects/id03_3dxrd/expt/RAW_DATA/FeAu_0p5_tR/FeAu_0p5_tR_ff1/scan0001",
        },
        "flt_3dpeaks_file_for_fine_refine": "/data/projects/id03_3dxrd/ewoks_test_data/grain_map/intensity_frac_0p9837_Fe_1p0100_filtered_3d_peaks.flt",
        "indexed_grain_ubi_file": "/data/projects/id03_3dxrd/ewoks_test_data/grain_map/Fe_grains.ubi",
        "flt_3dpeaks_file": "/data/projects/id03_3dxrd/ewoks_test_data/grain_map/intensity_frac_0p9837_Fe_all_filtered_3d_peaks.flt",
    }

    task = MakeGrainMap(inputs=inputs)
    task.execute()

    assert_grain_map_results(task.outputs)
