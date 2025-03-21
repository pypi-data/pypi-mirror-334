from ewokscore import Task
from pathlib import Path

from ImageD11 import columnfile as PeakColumnFile
from ImageD11.peakselect import sorted_peak_intensity_mask_and_cumsum


class FilterByIntensity(
    Task,
    input_names=[
        "peaks_3d_file",
        "intensity_frac",
    ],
    output_names=[
        "Ifilt_h5_col_file",
        "Ifilt_flt_col_file",
    ],
):
    """
    Does the Intensity based peaks filter,
        computes intensity metric based on sum_intensity, ds (reciprocal distance) columns from the input file
        normalize with the maximum value of intensity metric,
        only keeps the rows whose value is above the given input 'intensity_frac'
        and save them in ascii (.flt) and .h5 format.

    Inputs:

    - `peaks_3d_file`: a 3d merged column file h5 file, it is must be corrected for geometry and detector
    - `intensity_frac`: float value to remove the peaks row whose intensity metric below than this value.

    Outputs:

    - `Ifilt_h5_col_file`:  the rest of the strong peaks were saved as .h5 file path.
    - `Ifilt_flt_col_file`: the same .h5 file in .flt (ascii) format.
    """

    def run(self):
        peaks_3d_file = Path(self.inputs.peaks_3d_file)
        intensity_frac = self.inputs.intensity_frac
        if not peaks_3d_file.exists():
            raise FileNotFoundError(
                f"Input 3d peaks file {peaks_3d_file} does not exist."
            )

        cf = PeakColumnFile.columnfile(filename=str(peaks_3d_file))
        mask, _ = sorted_peak_intensity_mask_and_cumsum(colf=cf, frac=intensity_frac)
        cf.filter(mask)
        file_tag = f"{intensity_frac:.4f}".replace(".", "p")
        flt_file_path = (
            peaks_3d_file.parent / f"intensity_frac_{file_tag}_{peaks_3d_file.stem}.flt"
        )
        cf.writefile(str(flt_file_path))
        h5_file_path = flt_file_path.with_suffix(".h5")
        PeakColumnFile.colfile_to_hdf(cf, str(h5_file_path))
        self.outputs.Ifilt_h5_col_file = str(h5_file_path)
        self.outputs.Ifilt_flt_col_file = str(flt_file_path)
