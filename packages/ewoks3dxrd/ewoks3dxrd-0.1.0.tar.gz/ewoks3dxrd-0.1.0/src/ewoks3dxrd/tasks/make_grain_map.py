from __future__ import annotations

from pathlib import Path

from ewokscore import Task
from ImageD11 import grain as grainMod

from ..models import SampleConfig
from ..utils import (
    extract_sample_info,
    get_omega_slope,
    refine_grains,
    tmp_processing_files,
)


class MakeGrainMap(
    Task,
    input_names=[
        "folder_file_config",
        "indexed_grain_ubi_file",
        "flt_3dpeaks_file",
        "hkl_tols",
        "minpks",
        "lattice_name",
    ],
    optional_input_names=[
        "flt_3dpeaks_file_for_fine_refine",
        "intensity_two_theta_range",
        "symmetry",
    ],
    output_names=["ascii_grain_map_file"],
):
    """
    Does an iterative refinement based on `hkl_tols` followed by a fine refinement on the indexed grains

    Inputs:

    - `folder_file_config`: Output from Init Folder File Config Task as input here.
    - `indexed_grain_ubi_file`: indexed Grains ascii file path.
    - `flt_3dpeaks_file`: Filtered peaks column file path that were used for the indexing
    - `hkl_tols`: Decreasing sequence of hkl tolerances. Will be used for iterative refinement (one after the other).
    - `minpks`: To filter grains that are not associated with at least #minpks peaks after iterative refinement.
    - `lattice_name`: Use lattice parameter value from lattice par file referred by 'lattice_name'.par.

    Optional Inputs:

    - `flt_3dpeaks_file_for_fine_refine`: Peaks used to refine the grains finely at the end of the iterative refinement. Default: same file as `flt_3dpeaks_file`.
    - `intensity_two_theta_range`: tuple of two floats, giving two theta min and max when refining. Default: (0., 180.).
    - `symmetry` (str): Lattice symmetry used to further refine grains. Default: `cubic`.

    Outputs:
    - `ascii_grain_map_file`: file where the refined grains are saved
    """

    def run(self):
        ubi_grain_file = Path(self.inputs.indexed_grain_ubi_file)
        if not ubi_grain_file.exists():
            raise FileNotFoundError(
                f"Provided Indexed Ubi grain file: {ubi_grain_file} not found."
            )
        flt_pks_file = Path(self.inputs.flt_3dpeaks_file)
        if not flt_pks_file.exists():
            raise FileNotFoundError(
                f"Provided filtered Peaks File: {flt_pks_file} not found."
            )

        fine_flt_pks_file = self.get_input_value(
            "flt_3dpeaks_file_for_fine_refine", flt_pks_file
        )
        if not isinstance(fine_flt_pks_file, Path):
            fine_flt_pks_file = Path(fine_flt_pks_file)

        if not fine_flt_pks_file.exists():
            raise FileNotFoundError(
                f"Provided filtered Peaks File: {fine_flt_pks_file} not found."
            )

        cfg = SampleConfig(**self.inputs.folder_file_config)
        omega_motor = cfg.omega_motor
        scan_folder = cfg.scan_folder
        _, sample_name, dset_name, scan_number = extract_sample_info(
            path_str=scan_folder
        )
        master_file = Path(scan_folder).parent / f"{sample_name}_{dset_name}.h5"
        if not master_file.exists():
            raise FileNotFoundError(
                f"""Could not find HDF5 master file at {master_file}.
                    Check `scan_folder`, `sample_name` and `dset_name` in the `folder_file_config` input.
                """
            )

        error_message = []
        minpks = self.inputs.minpks
        if minpks <= 0:
            error_message.append("Input: 'minpks' should be a positive number")
        lattice_name = self.inputs.lattice_name
        lattice_par_file = ubi_grain_file.parent / "par_folder" / f"{lattice_name}.par"
        if not lattice_par_file.exists():
            error_message.append(
                f"Expected a lattice par file at {lattice_par_file}."
                "Perhaps the lattice_name is wrong?"
                "Or Lattice based peak filtering was not done?"
            )
        geo_par_file = ubi_grain_file.parent / "par_folder" / "geometry_tdxrd.par"
        if not geo_par_file.exists():
            error_message.append(
                f"Expected a geometry_tdxrd file at {geo_par_file}."
                "Perhaps geometry transformation was not done?"
            )
        if error_message:
            raise ValueError("\n".join(error_message))

        omega_slope = get_omega_slope(
            filepath=master_file, scan_number=scan_number, omega_motor=omega_motor
        )

        with tmp_processing_files(
            initial_ubi_file=ubi_grain_file,
            geo_par_file=geo_par_file,
            lattice_par_file=lattice_par_file,
        ) as (ubi_file, par_file):
            hkl_tols = self.inputs.hkl_tols
            intensity_tth_range = self.get_input_value(
                "intensity_two_theta_range", (0.0, 180.0)
            )
            symmetry = self.get_input_value("symmetry", "cubic")
            for tol in hkl_tols:
                iterative_refined_grains = refine_grains(
                    tolerance=tol,
                    intensity_tth_range=intensity_tth_range,
                    omega_slope=omega_slope,
                    parameter_file=par_file,
                    filtered_peaks_file=flt_pks_file,
                    ubi_file=ubi_file,
                    symmetry=symmetry,
                )
                iterative_refined_grains.savegrains(ubi_file, sort_npks=True)

            refined_grains = grainMod.read_grain_file(ubi_file)
            grains_filtered = [
                grain for grain in refined_grains if float(grain.npks) > minpks
            ]
            grainMod.write_grain_file(filename=ubi_file, list_of_grains=grains_filtered)

            # fine refinement
            fine_refined_grains = refine_grains(
                tolerance=hkl_tols[-1],
                intensity_tth_range=intensity_tth_range,
                omega_slope=omega_slope,
                parameter_file=par_file,
                filtered_peaks_file=fine_flt_pks_file,
                ubi_file=ubi_file,
                symmetry=symmetry,
            )

        output_grain_map_file = str(
            ubi_grain_file.parent / f"refined_grains_map_by_{lattice_name}.map"
        )
        fine_refined_grains.savegrains(output_grain_map_file, sort_npks=True)
        self.outputs.ascii_grain_map_file = output_grain_map_file
