from ewokscore import Task
from pathlib import Path
from ImageD11 import frelon_peaksearch

from ..models import (
    SegmenterConfig,
    SegmenterFolderConfig,
    SegmenterCorrectionFiles,
)
from ..utils import extract_sample_info, get_frame_image


class SegmentFrame(
    Task,
    input_names=["folder_config", "segmenter_algo_params", "correction_files"],
    output_names=[
        "raw_image",
        "bg_corrected_image",
        "found_peaks",
    ],
):
    """
    This task produces single segmented frame
    """

    def run(self):

        seg_folder_config = SegmenterFolderConfig(**self.inputs.folder_config)
        detector = seg_folder_config.detector
        scan_folder = seg_folder_config.scan_folder
        _, sample_name, dset_name, scan_number = extract_sample_info(
            path_str=scan_folder
        )
        masterfile_path = Path(scan_folder).parent / f"{sample_name}_{dset_name}.h5"
        raw_image = get_frame_image(
            file_path=masterfile_path,
            detector=detector,
            scan_id=scan_number + ".1",
        )
        raw_image = raw_image.astype("uint16")

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
        image_worker = frelon_peaksearch.worker(**segmenter_settings)
        goodpeaks = image_worker.peaksearch(img=raw_image, omega=0)
        # 23 and 24 are the columns for fast_column index and slow column index
        peak_positions = goodpeaks[:, 23:25].T

        self.outputs.raw_image = raw_image
        self.outputs.bg_corrected_image = image_worker.smoothed
        self.outputs.found_peaks = peak_positions
