from pathlib import Path

import h5py
import yaml


def get_path_of_version_file() -> Path:
    return Path(__file__).resolve().parent / '_data_versions.yaml'


def get_latest_pipeline_versions() -> dict:
    with open(get_path_of_version_file()) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def current_dataset_is_up_to_date(file: h5py.File, dataset_path: str, latest_version: int) -> bool:
    return file[dataset_path].attrs['version'] == latest_version


def dataset_exists(file: h5py.File, dataset_path: str) -> bool:
    try:
        file[dataset_path]
        return True
    except KeyError:
        return False
