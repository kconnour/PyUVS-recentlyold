import h5py
import numpy as np

from pyuvs.data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists


compression = 'gzip'
compression_opts = 4


def add_pixel_geometry_data_to_file(file: h5py.File, pixel_geometry_path: str) -> None:
    pass