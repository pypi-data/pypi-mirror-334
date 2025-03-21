import pytest

from ewoks3dxrd.utils import read_lattice_cell_data


@pytest.mark.parametrize("space_group", (229, "I"))
def test_read_lattice_cell_data(tmp_path, space_group):
    par_file = tmp_path / "Fe.par"
    with open(par_file, "w") as f:
        f.write(
            f"""cell__a 2.8694
cell__b 2.8694
cell__c 2.8694
cell_alpha 90.0
cell_beta 90.0
cell_gamma 90.0
cell_lattice_[P,A,B,C,I,F,R] {space_group}
"""
        )

    unit_cell_parameters = read_lattice_cell_data(par_file)

    assert unit_cell_parameters.a == 2.8694
    assert unit_cell_parameters.b == 2.8694
    assert unit_cell_parameters.c == 2.8694
    assert unit_cell_parameters.alpha == 90
    assert unit_cell_parameters.beta == 90
    assert unit_cell_parameters.gamma == 90
    assert unit_cell_parameters.space_group == space_group
