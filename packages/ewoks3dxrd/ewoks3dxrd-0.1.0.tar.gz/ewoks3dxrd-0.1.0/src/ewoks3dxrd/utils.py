from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Tuple, Generator

import h5py
import numpy as np
from ImageD11 import blobcorrector
from ImageD11 import columnfile as PeakColumnFile
from ImageD11.grain import grain as Grain
from ImageD11.refinegrains import refinegrains as RefineGrains
from tqdm import tqdm

from .models import UnitCellParameters


class TqdmProgressCallback(tqdm):
    def __init__(self, *args, TaskInstance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.TaskInstance = TaskInstance
        self.finished_count = 0

    def update(self, n: int = 1):
        super().update(n)
        self.finished_count += n
        if self.TaskInstance:
            self.TaskInstance.progress = 100.0 * (self.finished_count / self.total)


def correct_column_file(filename: str | Path, correction_files: Tuple[str, str] | str):
    segmented_columnfile_3d = PeakColumnFile.columnfile(filename=filename)
    peak_3d_dict = {
        title: segmented_columnfile_3d[title]
        for title in segmented_columnfile_3d.keys()
    }
    peak_3d_dict["spot3d_id"] = np.arange(len(peak_3d_dict["s_raw"]))
    raw_columnfile_3d = PeakColumnFile.colfile_from_dict(peak_3d_dict)

    if isinstance(correction_files, str):
        splinefile = correction_files
        return blobcorrector.correct_cf_with_spline(raw_columnfile_3d, splinefile)

    if isinstance(correction_files, tuple) and len(correction_files) == 2:
        e2dxfile, e2dyfile = correction_files
        return blobcorrector.correct_cf_with_dxdyfiles(
            raw_columnfile_3d, e2dxfile, e2dyfile
        )

    raise ValueError(
        f"Detector Spatial correction cannot be performed unless a spline file or a couple of e2dx, ed2dy files is provided. Got {correction_files}."
    )


def load_par_file(filepath: str | Path) -> dict:
    """
    Read .par file, and return each line as key, value pair
    """
    read_parameters = {}

    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                raise ValueError(f"Invalid line format: {line.strip()}")
            key, value = parts
            read_parameters[key] = value

    return read_parameters


def read_lattice_cell_data(lattice_data_file_path: str | Path) -> UnitCellParameters:
    """
    Reads lattice cell data from a file and extracts the lattice parameters and space group.
    """
    return UnitCellParameters(**load_par_file(lattice_data_file_path))


def save_grains_to_nexus(
    nexus_filename: str | Path,
    geometry_par_path: str | Path,
    lattice_par_file: str | Path,
    lattice_name: str,
    grains: List[Grain],
) -> None:
    """
    Save grain information (UBI matrices, lattice parameters) and
    the experiment geometry into a NeXus file.

    Parameters:
    - nexus_filename: Output NeXus file path
    - geometry_par_path: Path to the geometry_tdxrd.par file
    - lattice_par_file: Path to lattice parameters file
    - lattice_name: Name of the lattice type
    - grains (list of grain instances): List of grain objects with:
        - grain.ubi: (3,3) array
    """

    unit_cell_parameters = read_lattice_cell_data(
        lattice_data_file_path=lattice_par_file
    )
    lattice_parameters, space_group = (
        unit_cell_parameters.lattice_parameters,
        unit_cell_parameters.space_group,
    )

    with open(geometry_par_path, "r") as f:
        geometry_lines = [line.strip() for line in f]
    geometry_par = "\n".join(geometry_lines)

    num_grains = len(grains)
    ubi_matrices = np.zeros((num_grains, 3, 3), dtype=grains[0].ubi.dtype)
    translations = np.full((num_grains, 3), fill_value=np.nan)

    for i, grain in enumerate(grains):
        ubi_matrices[i] = grain.ubi
        if grain.translation:
            translations[i] = grain.translation

    with h5py.File(nexus_filename, "w") as f:
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        index_grains = entry.create_group("indexed_grains")
        index_grains.attrs["NX_class"] = "NXprocess"
        parameters_group = index_grains.create_group("parameters")
        parameters_group.attrs["NX_class"] = "NXcollection"
        parameters_group.create_dataset("geometry_par", data=geometry_par)
        parameters_group.create_dataset("lattice_name", data=lattice_name)
        parameters_group.create_dataset(
            "lattice_parameters", data=np.array(lattice_parameters)
        )
        if isinstance(space_group, int):
            parameters_group.create_dataset("space_group_number", data=space_group)
        else:
            parameters_group.create_dataset("space_group_symbol", data=space_group)

        grains_group = index_grains.create_group("grains")
        grains_group.attrs["NX_class"] = "NXdata"
        grains_group.create_dataset("UBI", data=ubi_matrices)
        grains_group.create_dataset("translation", data=translations)


def read_wavelength(geometry_par_file: str | Path) -> float:
    with open(geometry_par_file, "r") as f:
        for line in f:
            if line.startswith("wavelength"):
                try:
                    wavelength = float(line.strip().split()[1])
                    break
                except (IndexError, ValueError):
                    raise ValueError(
                        f"Could not found a valid wavelength field in {geometry_par_file}"
                    )
    return wavelength


def get_omega_slope(filepath, scan_number, omega_motor):
    with h5py.File(filepath, "r") as hin:
        omega_angles = hin[f"{scan_number}.1/measurement"].get(omega_motor, None)
        omega_array = omega_angles[()]

    omegas_sorted = np.sort(omega_array)
    omega_step = np.round(np.diff(omegas_sorted).mean(), 3)
    return omega_step / 2


def refine_grains(
    tolerance: float,
    intensity_tth_range: Tuple[float, float],
    omega_slope: float,
    symmetry: str,
    parameter_file: str | Path,
    filtered_peaks_file: str | Path,
    ubi_file: str | Path,
) -> RefineGrains:
    refined_grains = RefineGrains(
        tolerance=tolerance,
        intensity_tth_range=intensity_tth_range,
        OmSlop=omega_slope,
    )
    refined_grains.loadparameters(str(parameter_file))
    refined_grains.loadfiltered(str(filtered_peaks_file))
    refined_grains.readubis(str(ubi_file))
    refined_grains.makeuniq(symmetry)
    refined_grains.generate_grains()
    refined_grains.refinepositions()

    return refined_grains


def extract_sample_info(path_str: str) -> Tuple[str, str, str, str]:
    """
    Helper function to extract the dataroot, sample, dset_name, scan no from the
    scan folder path
    """
    path = Path(path_str)
    if len(path.parts) < 4:
        raise ValueError(
            "Expected path structure to be of the for `/dataroot/sample_name/dset_name/scan_number`"
        )

    # check provided path is actually a scan folder
    if len(path_str) < 8 or path_str[-8:-4] != "scan":
        raise ValueError(
            f"Invalid scan folder path: '{path_str}' should end with `scanxxxx` where xxxx are numbers"
        )

    # Extract scan number (last 4 digits)
    try:
        scan_number = int(path.name[-4:])
    except (ValueError, IndexError):
        raise ValueError(f"Expected {path.name} to end with 4 numbers.")

    # Extract dset name
    dset_folder_name = path.parent.name
    if "_" not in dset_folder_name:
        raise ValueError(
            f"Invalid dataset name: no underscore found in {dset_folder_name} to separate sample and dataset name.",
        )

    dataroot = path.parent.parent.parent.__str__()
    sample_name = path.parent.parent.name
    dset_name = dset_folder_name[len(sample_name + "_") :]
    return dataroot, sample_name, dset_name, str(scan_number)


def get_frame_image(
    file_path: str | Path,
    detector: str,
    scan_id: str,
    frame_idx: int | None = None,
    counter: str = "_roi1",
):
    """
    extract a frame image from master file path
    """
    with h5py.File(file_path, "r") as h5file:
        if frame_idx is None:
            detector_ctr = detector + counter
            frame_idx = np.argmax(h5file[f"{scan_id}/measurement/{detector_ctr}"][:])
        return h5file[f"{scan_id}/measurement/{detector}"][frame_idx]


@contextmanager
def tmp_processing_files(
    initial_ubi_file: str | Path, geo_par_file: str | Path, lattice_par_file: str | Path
) -> Generator[Tuple[str, str], None, None]:
    _, tmp_ubi_file = tempfile.mkstemp()
    _, tmp_par_file = tempfile.mkstemp()

    try:
        shutil.copy2(initial_ubi_file, tmp_ubi_file)

        with open(tmp_par_file, "w") as file:
            geometry_parameters = load_par_file(geo_par_file)
            for key, value in geometry_parameters.items():
                file.write(f"{key} {value}\n")

            lattice_parameters = load_par_file(lattice_par_file)
            for key, value in lattice_parameters.items():
                file.write(f"{key} {value}\n")

        yield tmp_ubi_file, tmp_par_file
    finally:
        os.remove(tmp_ubi_file)
        os.remove(tmp_par_file)
