from __future__ import annotations

from pathlib import Path

from ewokscore import Task
from ImageD11 import columnfile as PeakColumnFile
from ImageD11 import grain, indexing
from ImageD11.unitcell import unitcell

from ..utils import (
    read_lattice_cell_data,
    read_wavelength,
    save_grains_to_nexus,
)


class IndexGrains(
    Task,
    input_names=[
        "flt_peaks_3d_file",
        "gen_rings_from_idx",
        "score_rings_from_idx",
        "lattice_name",
    ],
    optional_input_names=[
        "max_grains",
        "reciprocal_dist_tol",
        "hkl_tols",
        "min_pks_frac",
        "cosine_tol",
    ],
    output_names=["grain_ubi_file", "grain_nexus_file"],
):
    """
    From 3D peaks, finds grains' UBI  matrices and stores them in both ASCII format and NeXus (.h5) format.

    Inputs:

    - `flt_peaks_3d_file` (str): File containing lattice and intensity filtered 3d merged peaks.
    - `gen_rings_from_idx` (Tuple): Indices of rings used for generating UBI. Two are usually enough, three in some rare cases.
    - `score_rings_from_idx` (Tuple): Indices of the rings used for scoring. These must contain the indices used for indexing.
    - `lattice_name` (str): lattice name indicating {lattice_name}.par file
            a parameter file inside the par_folder

    Optional Inputs:

    - `max_grains` (int): To limit the maximum number of grains (UBI matrices).
    - `reciprocal_dist_tol` (float): reciprocal distance tolerance value.
    - `hkl_tols` (Tuple): hkl tolerance, (hkl are integers, while doing convergence, had to do discretization on processed values)
    - `min_pks_frac` (Tuple): min peaks fraction to iterate over
    - `cosine_tol` (float): a tolerance value used in the Indexer convergence scheme
        for finding pairs of peaks to make an orientation

    Outputs:

    - `grain_ubi_file` (str): Path to the ASCII file that stores the generated UBI
    - `grain_nexus_file` (str): Path to the NeXus file that stores the computed grains along with lattice parameter,
            geometry_tdxrd information etc.
    """

    def run(self):
        ph_flt_h5_file = Path(self.inputs.flt_peaks_3d_file)
        gen_rings_idx = self.inputs.gen_rings_from_idx
        score_rings_idx = self.inputs.score_rings_from_idx
        lattice_name = self.inputs.lattice_name

        indexing_params = {}
        if self.get_input_value("max_grains", None):
            indexing_params["max_grains"] = self.inputs.max_grains
        if self.get_input_value("reciprocal_dist_tol", None):
            indexing_params["dstol"] = self.inputs.reciprocal_dist_tol
        if self.get_input_value("hkl_tols", None):
            indexing_params["hkl_tols"] = self.inputs.hkl_tols
        if self.get_input_value("min_pks_frac", None):
            indexing_params["fracs"] = self.inputs.min_pks_frac
        if self.get_input_value("cosine_tol", None):
            indexing_params["cosine_tol"] = self.inputs.cosine_tol

        error_message = []

        if not ph_flt_h5_file.exists():
            error_message.append(
                f"Filtered 3d peaks file '{ph_flt_h5_file}' not found."
            )
        if len(gen_rings_idx) < 2:
            error_message.append(
                f"UBI needs at least two ring indices in `gen_rings_idx`. Got {gen_rings_idx}"
            )

        work_folder = ph_flt_h5_file.parent
        lattice_par_file = work_folder / f"par_folder/{lattice_name}.par"
        if not lattice_par_file.exists():
            error_message.append(
                f"Expected a lattice par file at {lattice_par_file}. Perhaps the lattice_name is wrong?"
                "in the parent folder of provided lattice filtered 3d peaks file: "
                f"{ph_flt_h5_file}"
            )
        if error_message:
            raise ValueError("\n".join(error_message))

        filtered_cf = PeakColumnFile.columnfile(filename=str(ph_flt_h5_file))
        unit_cell_parameters = read_lattice_cell_data(
            lattice_data_file_path=lattice_par_file
        )
        unit_cell = unitcell(
            lattice_parameters=unit_cell_parameters.lattice_parameters,
            symmetry=unit_cell_parameters.space_group,
        )
        unit_cell.makerings(limit=filtered_cf.ds.max())
        geometry_par_file = work_folder / "par_folder" / "geometry_tdxrd.par"
        if not geometry_par_file.exists():
            raise FileNotFoundError(f"Expected a geometry file at {geometry_par_file}")
        wavelength = read_wavelength(geometry_par_file)
        grains, _ = indexing.do_index(
            cf=filtered_cf,
            forgen=gen_rings_idx,
            foridx=score_rings_idx,
            unitcell=unit_cell,
            wavelength=wavelength,
            **indexing_params,
        )

        # have to save the grains, and ubi matrices.
        grain_ubi_file_path = str(work_folder / f"{lattice_name}_grains.ubi")
        grain.write_grain_file(grain_ubi_file_path, grains)
        grain_nexus_file = str(work_folder / f"{lattice_name}_grains.h5")
        save_grains_to_nexus(
            nexus_filename=grain_nexus_file,
            geometry_par_path=geometry_par_file,
            lattice_par_file=lattice_par_file,
            lattice_name=lattice_name,
            grains=grains,
        )
        self.outputs.grain_ubi_file = grain_ubi_file_path
        self.outputs.grain_nexus_file = grain_nexus_file
