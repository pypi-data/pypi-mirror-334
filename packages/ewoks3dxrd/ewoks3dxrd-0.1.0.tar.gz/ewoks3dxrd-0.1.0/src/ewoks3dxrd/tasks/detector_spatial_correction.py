from ewokscore import Task
from pathlib import Path

from ImageD11 import columnfile as PeakColumnFile

from ..utils import correct_column_file


class DetectorSpatialCorrection(
    Task,
    input_names=["segmented_3d_peaks_file", "correction_files"],
    output_names=["detector_spatial_corrected_3d_peaks_file"],
):
    """
    Does the detector spatial correction on the segmented 3d peaks and saves the corrected 3D column peak file

    Inputs:

    - `segmented_3d_peaks_file`: a 3d peaks columnfile saved as hdf5 file
    - `correction_files`: two corrections are possible:
        - Spline correction: `correction_files` should be a string containing the path to the spline file
        - e2dx,e2dy correction: `correction_files` should be a tuple of 2 strings, the first one being the path to e2dx file, the second the path to the e2dy file
        - any other type will be treated as invalid input

    Outputs:
    - `detector_spatial_corrected_3d_peaks_file`: file where the resulting detector detector spatial corrected 3d peaks are saved
    """

    def run(self):
        segmented_3d_columnfile_h5 = Path(self.inputs.segmented_3d_peaks_file)
        detector_spatial_correction_file_lists = self.inputs.correction_files

        if not Path(segmented_3d_columnfile_h5).exists():
            raise FileNotFoundError(
                f""" Provided segmented 3d columnfile path: {segmented_3d_columnfile_h5} does not exist.
                """
            )

        columnfile_3d = correct_column_file(
            segmented_3d_columnfile_h5, detector_spatial_correction_file_lists
        )
        parent_folder_segmented_3d_columnfile = Path(segmented_3d_columnfile_h5).parent
        detector_spatial_corrected_3d_peaks_file = (
            parent_folder_segmented_3d_columnfile
            / "detector_spatial_corrected_3d_peaks.h5"
        )
        PeakColumnFile.colfile_to_hdf(
            columnfile_3d, str(detector_spatial_corrected_3d_peaks_file)
        )

        self.outputs.detector_spatial_corrected_3d_peaks_file = str(
            detector_spatial_corrected_3d_peaks_file
        )
