from ewokscore import Task
from pathlib import Path
import shutil

from ImageD11 import columnfile as PeakColumnFile


class GeometryTransformation(
    Task,
    input_names=[
        "spatial_corrected_peaks_3d_file",
        "geometry_par_file",
    ],
    output_names=["geometry_updated_3d_peaks_file"],
):
    """
    Does the geometry Transformation on the detector spatial corrected 3d peaks file
    and geometry parameter (.par) file,
    Inputs:
        '3d_peaks_file'
        a detector spatial corrected 3d peaks columnfile as .h5 and
        geometry file path a .par file
    This task performs the following operations:
    1. Gathers geometry information from the `geometry_tdxrd.par` file.
    2. Copy the geometry file in the directory structure:
            `analysis_folder / dset_name / (dset_name + sample_name)`.
            i.e the parent folder of 'detector_spatial_corrected_3d_peaks_file'
    3. Applies the geometry correction to the 3D peaks column file using
        the `ImageD11` dataset class.
    4. Save the geometry corrected 3d peaks columnfile (output: `geometry_updated_3d_peaks_file`)
    """

    def run(self):
        seg_3d_col_file = self.inputs.spatial_corrected_peaks_3d_file
        geometry_par_file = self.inputs.geometry_par_file

        error_message = []
        if not Path(geometry_par_file).exists():
            error_message.append(f"Geometry file '{geometry_par_file}' not found.")

        if not geometry_par_file.endswith(".par"):
            error_message.append(
                f"Invalid geometry file '{geometry_par_file}'. Expected a '.par' file."
            )

        if not Path(seg_3d_col_file).exists():
            error_message.append(
                f"Provided '{seg_3d_col_file}' spatial corrected and segmented 3D peak file is missing."
            )

        if error_message:
            raise ValueError("\n".join(error_message))

        work_folder = Path(seg_3d_col_file).parent
        par_folder = work_folder / "par_folder"
        par_folder.mkdir(exist_ok=True)
        new_geometry_par_file = par_folder / "geometry_tdxrd.par"
        shutil.copy2(geometry_par_file, new_geometry_par_file)

        # following code is derived by refering:
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/sinograms/dataset.py
        # refer at function  update_colfile_pars()
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/parameters.py
        # refer at function loadparameters() in the class 'parameters' (yes it is a class not function)
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/columnfile.py
        # refer at function updateGeometry() in the class 'columnfile' (yes it is a class not function)
        # as for as my investigation, it does not do any computation,
        # but with the style of imageD11 library, it adds various geometry parameter from
        # geometry_tdxrd.par file into the column file,
        columnfile_3d = PeakColumnFile.columnfile(filename=seg_3d_col_file)
        columnfile_3d.parameters.loadparameters(filename=str(new_geometry_par_file))
        columnfile_3d.updateGeometry()
        geometry_updated_3d_peaks_file = work_folder / "geometry_updated_3d_peaks.h5"
        PeakColumnFile.colfile_to_hdf(
            columnfile_3d, str(geometry_updated_3d_peaks_file)
        )
        self.outputs.geometry_updated_3d_peaks_file = str(
            geometry_updated_3d_peaks_file
        )
