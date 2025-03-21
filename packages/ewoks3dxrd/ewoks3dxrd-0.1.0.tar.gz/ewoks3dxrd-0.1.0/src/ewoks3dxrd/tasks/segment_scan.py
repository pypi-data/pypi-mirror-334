from ewokscore import TaskWithProgress

from ImageD11 import frelon_peaksearch
from ImageD11 import columnfile as PeakColumnFile

from ..models import (
    SegmenterConfig,
    SegmenterFolderConfig,
    SegmenterCorrectionFiles,
)
from ..utils import TqdmProgressCallback, extract_sample_info
from pathlib import Path
import h5py


class SegmentScan(
    TaskWithProgress,
    input_names=["folder_config", "segmenter_algo_params", "correction_files"],
    output_names=["segmented_3d_peaks_file", "sample_folder_info"],
):
    """
    This task segments an entire scan folder,
    merges the peaks, and produces a 3D column file.
    The resulting 3D column peak file is saved.

    Outputs:

    - `segmented_3d_peaks_file`: A segmented 3d peaks for the given scan folder is saved in this path.
    - `sample_folder_info`: A Config information about raw scan sample
    """

    def run(self):

        seg_folder_config = SegmenterFolderConfig(**self.inputs.folder_config)

        detector = seg_folder_config.detector
        omega_motor = seg_folder_config.omega_motor
        scan_folder = seg_folder_config.scan_folder

        _, sample_name, dset_name, scan_number = extract_sample_info(
            path_str=scan_folder
        )

        masterfile_path = Path(scan_folder).parent / f"{sample_name}_{dset_name}.h5"
        if not masterfile_path.exists():
            raise FileNotFoundError(
                """ 'scan_folder' field in 'seg_folder_config' does not have master file
                        in its parent folder. From its parent folder, we will have its masterfile path.
                    This masterfile path required to compute Omega (rotation) values.
                """
            )
        analyse_folder = seg_folder_config.analyse_folder
        output_folder = (
            Path(analyse_folder) / sample_name / f"{sample_name}_{dset_name}"
        )
        output_folder.mkdir(parents=True, exist_ok=True)

        with h5py.File(str(masterfile_path), "r") as hin:
            omega_angles = hin[str(scan_number) + ".1"]["measurement"].get(
                omega_motor, None
            )
            omega_array = omega_angles[()]

        segmenter_cfg = SegmenterConfig(**self.inputs.segmenter_algo_params)
        correction_files_config = SegmenterCorrectionFiles(
            **self.inputs.correction_files
        )
        segmenter_settings = {
            "bgfile": correction_files_config.bg_file,
            "maskfile": correction_files_config.mask_file,
            "darkfile": correction_files_config.dark_file,
            "flatfile": correction_files_config.flat_file,
            "threshold": segmenter_cfg.threshold,
            "smoothsigma": segmenter_cfg.smooth_sigma,
            "bgc": segmenter_cfg.bgc,
            "minpx": segmenter_cfg.min_px,
            "m_offset_thresh": segmenter_cfg.offset_threshold,
            "m_ratio_thresh": segmenter_cfg.ratio_threshold,
        }

        all_frames_2d_peaks_list = frelon_peaksearch.segment_master_file(
            str(masterfile_path),
            str(scan_number) + ".1" + "/measurement/" + detector,
            omega_array,
            segmenter_settings,
            tqdm_class=TqdmProgressCallback,
            TaskInstance=self,
        )
        peaks_2d_dict, num_peaks = frelon_peaksearch.peaks_list_to_dict(
            all_frames_2d_peaks_list
        )
        # 3d merge from 2d peaks dict
        peak_3d_dict = frelon_peaksearch.do3dmerge(
            peaks_2d_dict, num_peaks, omega_array
        )
        segmented_columnfile_3d = PeakColumnFile.colfile_from_dict(peak_3d_dict)
        segmented_3d_columnfile_h5 = f"{analyse_folder}/{sample_name}/{sample_name}_{dset_name}/segmented_3d_peaks.h5"
        PeakColumnFile.colfile_to_hdf(
            segmented_columnfile_3d, segmented_3d_columnfile_h5
        )
        self.outputs.segmented_3d_peaks_file = segmented_3d_columnfile_h5
        self.outputs.sample_folder_info = {
            "omega_motor": omega_motor,
            "scan_folder": scan_folder,
        }
