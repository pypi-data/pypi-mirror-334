from ewokscore import Task
from pathlib import Path
import shutil

from ImageD11 import columnfile as PeakColumnFile
from ..utils import read_lattice_cell_data
from ImageD11.unitcell import unitcell
from ImageD11.peakselect import filter_peaks_by_phase


class FilterByLattice(
    Task,
    input_names=[
        "geometry_trans_3d_peaks_file",
        "lattice_par_file",
        "reciprocal_dist_tol",
    ],
    optional_input_names=["reciprocal_dist_max"],
    output_names=[
        "filtered_h5_col_file",
        "filtered_flt_col_file",
        "copied_lattice_par_file",
    ],
):
    """
    Performs Lattice/Phase-based filtering on a geometry-transformed 3D peaks file.

    This process applies filtering based on 'reciprocal distance' and 'lattice' rings ds criteria
    to extract relevant peaks.

    ### Steps:
    1. **Initial Filtering:**
        - Copies the input geometry-transformed 3D peaks file.
        - Reads the `ds` column and removes rows where `ds` exceeds the specified `reciprocal_dist_max` value.

    2. **Lattice-Based Filtering:**
        - Computes ideal lattice ring `ds` values (reciprocal distances from the origin).
        - Further filters peaks based on these values, using the tolerance defined by `reciprocal_dist_tol`.

    3. **File Storage:**
        - Saves the lattice-filtered 3D peaks file as
            `{Lattice_name}_{reciprocal_dist_max_tag}_filtered_3d_peaks.h5,flt`
            in the parent directory of the input file ('geometry_trans_3d_peaks_file').

    Additionally, if the specified `lattice_par_file` is not present in the sample analysis path,
    it is copied to `"par_folder/{lattice_par_file}"`.

    ### Inputs
    - `geometry_trans_3d_peaks_file` (str): Path to the geometry-transformed `.h5` 3D peaks file.
    - `lattice_par_file` (str): Path to the `.par` file containing lattice parameters and space group information.
    - `reciprocal_dist_max` (float): Maximum reciprocal distance for filtering (an Optional Value)
        If it is not provided, then maximum value in the `ds` column from input file will be used.
    - `reciprocal_dist_tol` (float): Tolerance for peak inclusion near lattice rings.

    ### Outputs
    - `filtered_h5_col_file` (str): Path to the lattice-filtered `.h5` file, named as
    `{lattice_name}_{reciprocal_dist_max_tag}_filtered_3d_peaks.h5`.
    The `reciprocal_dist_max_tag` is either `'all'` or formatted as `f"{dstar_max:.4f}".replace(".", "p")`.
    - `filtered_flt_col_file` (str): Path to the same filtered file in ASCII format (`.flt`).
    - `copied_lattice_par_file` (str): Path to the copied lattice parameter file stored within the analysis folder.
    """

    def run(self):
        geometry_trans_3d_peaks_file = Path(self.inputs.geometry_trans_3d_peaks_file)
        lattice_par_file = Path(self.inputs.lattice_par_file)
        dstar_tol = self.inputs.reciprocal_dist_tol
        error_message = []

        if not geometry_trans_3d_peaks_file.exists():
            error_message.append(
                f"Geometry file '{geometry_trans_3d_peaks_file}' not found."
            )
        if not lattice_par_file.exists():
            error_message.append(
                f"Provided Lattice file '{lattice_par_file}' does not exist."
            )
        if lattice_par_file.suffix != ".par":
            error_message.append(
                f"Provided Lattice file '{lattice_par_file}' is not a .par file"
            )
        if error_message:
            raise ValueError("\n".join(error_message))

        lattice_file_in_par_folder = (
            geometry_trans_3d_peaks_file.parent / "par_folder" / lattice_par_file.name
        )

        lattice_file_in_par_folder.parent.mkdir(exist_ok=True)
        shutil.copy2(lattice_par_file, lattice_file_in_par_folder)

        g_trans_peaks_3d = PeakColumnFile.columnfile(
            filename=str(geometry_trans_3d_peaks_file)
        )
        unit_cell_parameters = read_lattice_cell_data(lattice_par_file)

        lattice_name = lattice_par_file.stem
        reciprocal_dist_max: float | None = self.get_input_value(
            "reciprocal_dist_max", None
        )
        if reciprocal_dist_max:
            dstar_max = reciprocal_dist_max
            dstar_as_str = f"{dstar_max:.4f}".replace(".", "p")
            flt_file_name = f"{lattice_name}_{dstar_as_str}_filtered_3d_peaks.flt"

        else:
            dstar_max = g_trans_peaks_3d.ds.max()
            flt_file_name = f"{lattice_name}_all_filtered_3d_peaks.flt"

        cf = g_trans_peaks_3d.copyrows(g_trans_peaks_3d.ds <= dstar_max)
        ucell = unitcell(
            lattice_parameters=unit_cell_parameters.lattice_parameters,
            symmetry=unit_cell_parameters.space_group,
        )
        ucell.makerings(limit=g_trans_peaks_3d.ds.max())

        filtered_peaks_cf = filter_peaks_by_phase(
            cf=cf, dstol=dstar_tol, dsmax=dstar_max, cell=ucell
        )

        flt_file_path = geometry_trans_3d_peaks_file.parent / flt_file_name
        filtered_peaks_cf.writefile(str(flt_file_path))
        h5_file_path = flt_file_path.with_suffix(".h5")
        PeakColumnFile.colfile_to_hdf(filtered_peaks_cf, str(h5_file_path))

        self.outputs.filtered_h5_col_file = str(h5_file_path)
        self.outputs.filtered_flt_col_file = str(flt_file_path)
        self.outputs.copied_lattice_par_file = str(lattice_file_in_par_folder)
