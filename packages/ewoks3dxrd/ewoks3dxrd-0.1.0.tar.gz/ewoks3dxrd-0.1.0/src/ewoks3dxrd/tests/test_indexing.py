from ewoks3dxrd.tasks.index_grains import IndexGrains

from .conftest import assert_indexing_results


def test_indexing():
    filepath = "/data/projects/id03_3dxrd/ewoks_test_data/indexing/intensity_frac_0p9837_Fe_1p0100_filtered_3d_peaks.h5"

    inputs = {
        "flt_peaks_3d_file": filepath,
        "reciprocal_dist_tol": 0.05,
        "gen_rings_from_idx": (0, 1),
        "score_rings_from_idx": (0, 1, 2, 3),
        "lattice_name": "Fe",
        "hkl_tols": (0.01, 0.02, 0.03, 0.04),
        "min_pks_frac": (0.9, 0.75),
    }

    task = IndexGrains(inputs=inputs)
    task.execute()

    assert_indexing_results(task.outputs)
