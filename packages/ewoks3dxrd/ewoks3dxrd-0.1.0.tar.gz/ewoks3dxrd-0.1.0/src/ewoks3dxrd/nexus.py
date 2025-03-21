from __future__ import annotations

from pathlib import Path
from typing import Any, List, Tuple

import h5py
import numpy as np
from ImageD11 import grain as grainmod
from ImageD11.grain import grain as Grain


def create_parameters_group(
    parent_group: h5py.Group,
    config_settings: dict[str, Any],
    group_name: str = "parameters",
):
    """
    Helper function to place the config_settings in 'param_name' group
    in the given `parent_group`
    """
    parameters_group = parent_group.create_group(group_name)
    parameters_group.attrs["NX_class"] = "NXcollection"
    for key, value in config_settings.items():
        parameters_group.create_dataset(
            key, data=value if value is not None else "None"
        )


def save_nexus_segmentation(
    entry_name: str,
    filename: str | Path,
    seg_3d_data: dict[str, np.ndarray],
    config_set: dict[str, dict[str, Any]],
):
    """
    Save a 3D segmentation dataset into an HDF5 (NeXus) file.
    Inputs:
    - `entry_name`: Name of the parent entry where the segmenter process (group) will be saved.
    - `filename`: Path to the HDF5 file where data will be saved.
    - `seg_3d_data`: peaks column data sets.
    - `config_set`: Configuration parameters structured as nested dictionaries.
    """
    with h5py.File(filename, "w") as f:
        entry = f.create_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"

        segmentation_group = entry.create_group("segmented_3d_peaks")
        segmentation_group.attrs["NX_class"] = "NXprocess"

        peaks_group = segmentation_group.create_group("peaks")
        peaks_group.attrs["NX_class"] = "NXdata"

        for key, value in seg_3d_data.items():
            peaks_group.create_dataset(key, data=value)

        parameters_group = segmentation_group.create_group("parameters")
        parameters_group.attrs["NX_class"] = "NXcollection"

        for param_name, param_values in config_set.items():
            create_parameters_group(
                parent_group=parameters_group,
                config_settings=param_values,
                group_name=param_name,
            )


def create_peaks_column_group(
    filename: str | Path,
    entry_name: str,
    process_name: str,
    peaks_data: dict[str, np.ndarray],
    config_settings: dict[str, Any],
):
    """
    Create a NXprocess group to save peaks data and parameters
    Inputs:
        `filename`: file path to existing .h5 file
        `entry_name`: entry point in the .h5 file
        `data_group`: new group name inside the sample_dataset
        `peaks_data`: peaks column data sets
        `config_settings`: dict of configuration settings.
    """
    with h5py.File(filename, "a") as f:
        entry = f[entry_name]
        grp = entry.create_group(process_name)
        grp.attrs["NX_class"] = "NXprocess"
        peaks_group = grp.create_group("peaks")
        for key, value in peaks_data.items():
            peaks_group.create_dataset(key, data=value)

        create_parameters_group(parent_group=grp, config_settings=config_settings)


def read_peaks_attributes(
    filename: str | Path, entry_name: str, process_name: str
) -> dict[str, np.ndarray]:
    """
    Extract peaks column data stored in {entry_name}/{process_name}/peaks
    Inputs:
        filename: file path to .h5 file
        entry_name: entry point inside .h5 file
        process_name: group name inside the entry point
    """
    with h5py.File(filename, "r") as f:
        peaks_group = f[f"{entry_name}/{process_name}/peaks"]
        return {name: dataset[()] for name, dataset in peaks_group.items()}


def create_nexus_ubi(
    grains: List[Grain],
    entry_name: str,
    grain_file: str | Path,
    grain_settings: dict[str, Any],
    peaks_path: Tuple[str | Path, str],
):
    """
    Create nexus file with entry_name place the grains (list of UBIs)
    and also link the peaks used to generate these UBIS as external link
    """
    with h5py.File(grain_file, "w") as gf:
        entry = gf.create_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"
        grain_group = entry.create_group("indexed_grains")
        grain_group.attrs["NX_class"] = "NXprocess"
        grain_group["peaks"] = h5py.ExternalLink(peaks_path[0], peaks_path[1])
        ubi_group = grain_group.create_group("UBI")
        ubi_group.attrs["NX_class"] = "NXdata"
        ubi_matrices = ubi_group.create_dataset(
            "UBI", shape=(len(grains), 3, 3), dtype=grains[0].ubi.dtype
        )
        for i, grain in enumerate(grains):
            ubi_matrices[i] = grain.ubi
        create_parameters_group(
            parent_group=grain_group, config_settings=grain_settings
        )


def create_nexus_grains(
    grains: List[Grain],
    entry_name: str,
    grain_file: str | Path,
    grain_settings: dict[str, Any],
    grain_group_name: str,
):
    num_grains = len(grains)
    with h5py.File(grain_file, "a") as gf:
        entry = gf[entry_name]
        grp = entry.create_group(grain_group_name)
        grp.attrs["NX_class"] = "NXprocess"
        grains_gr = grp.create_group("grains")
        grains_gr.attrs["NX_class"] = "NXdata"

        ubi_matrices = grains_gr.create_dataset(
            "UBI", shape=(num_grains, 3, 3), dtype=grains[0].ubi.dtype
        )
        translations = grains_gr.create_dataset(
            "translation", shape=(num_grains, 3), dtype=grains[0].ubi.dtype
        )
        npks = grains_gr.create_dataset("npks", shape=(num_grains,), dtype=np.int64)
        nuniq = grains_gr.create_dataset("nuniq", shape=(num_grains,), dtype=np.int64)
        for i, grain in enumerate(grains):
            ubi_matrices[i] = grain.ubi
            translations[i] = grain.translation
            npks[i] = grain.npks
            nuniq[i] = grain.nuniq

        create_parameters_group(parent_group=grp, config_settings=grain_settings)


def save_indexed_grains_as_ascii(
    grain_file_h5: str | Path,
    entry_name: str,
    process_group_name: str,
    grain_file_ascii: str | Path,
):
    """
    Function to extract grains that generated by Indexing function,
    which is simpler, i.e it only has UBI matrices.
    """
    grains_list = []
    with h5py.File(grain_file_h5, "r") as gf:
        entry = gf[f"{entry_name}/{process_group_name}"]
        ubi_grp = entry["UBI"]
        for ubi_matrix in ubi_grp["UBI"]:
            grains_list.append(Grain(ubi=ubi_matrix))

    grainmod.write_grain_file(grain_file_ascii, grains_list)


def read_grains(
    grain_file_h5: str | Path, entry_name: str, process_group_name: str
) -> List[Grain]:

    grains_list = []
    with h5py.File(grain_file_h5, "r") as gf:
        entry = gf[f"{entry_name}/{process_group_name}/grains"]
        for i in range(entry["translation"][()].shape[0]):
            gr = Grain.grain(ubi=entry["UBI"][i], translation=entry["translation"][i])
            gr.npks = entry["npks"][i]
            gr.nuniq = entry["nuniq"][i]
            grains_list.append(gr)
    return grains_list


def get_omega_array(
    filename: str | Path, entry_name: str, process_group_name: str
) -> np.ndarray:
    with h5py.File(filename, "r") as f:
        entry = f[f"{entry_name}/{process_group_name}"]
        folder_grp = entry["parameters/FolderFileSettings"]
        masterfile = folder_grp["masterfile"][()].decode()
        scan_number = folder_grp["scan_number"][()].decode()
        omegamotor = folder_grp["omegamotor"][()].decode()
        with h5py.File(masterfile, "r") as hin:
            omega_angles = hin[f"{scan_number}.1/measurement"][omegamotor]
            return omega_angles[()]


def get_lattice_parameters(
    filename: str | Path, entry_name: str, process_group_name: str
) -> Tuple[np.ndarray, int]:
    with h5py.File(filename, "r") as f:
        entry = f[f"{entry_name}/{process_group_name}"]
        par_grp = entry["parameters"]
        lattice_parameters = par_grp["lattice_parameters"][()]
        symmetry = int(par_grp["lattice_space_group"][()])
    return lattice_parameters, symmetry


def get_wavelength(
    filename: str | Path, entry_name: str, process_group_name: str
) -> float:
    with h5py.File(filename, "r") as f:
        entry = f[f"{entry_name}/{process_group_name}"]
        par_grp = entry["parameters"]
        wavelength = float(par_grp["wavelength"][()])
    return wavelength


def get_parameters(
    filename: str | Path, entry_name: str, process_group_name: str
) -> dict[str, str]:
    par_dict = {}
    with h5py.File(filename, "r") as f:
        entry = f[f"{entry_name}/{process_group_name}"]
        par_grp = entry["parameters"]
        for key in par_grp.keys():
            value = par_grp[key][()]
            par_dict[key] = value.decode() if isinstance(value, bytes) else value
    return par_dict


def save_geometry_and_lattice_par_file(
    file_path: str | Path, geom_dict: dict[str, Any], lattice_dict: dict[str, Any]
):
    with open(file_path, "w") as f:
        lattice_params = lattice_dict.get("lattice_parameters", [])
        if len(lattice_params) != 6:
            raise ValueError(
                f"Expected a list of 6 lattice params. Got {lattice_params}"
            )
        f.write(f"cell__a {lattice_params[0]}\n")
        f.write(f"cell__b {lattice_params[1]}\n")
        f.write(f"cell__c {lattice_params[2]}\n")
        f.write(f"cell_alpha {lattice_params[3]}\n")
        f.write(f"cell_beta {lattice_params[4]}\n")
        f.write(f"cell_gamma {lattice_params[5]}\n")

        if "lattice_space_group" in lattice_dict:
            f.write(
                f"cell_lattice_[P,A,B,C,I,F,R] {lattice_dict['lattice_space_group']}\n"
            )

        for key, value in geom_dict.items():
            f.write(f"{key} {value}\n")
