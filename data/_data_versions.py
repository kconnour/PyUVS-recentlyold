from pathlib import Path

import yaml

from _structure import DataFile


def get_path_of_integration_version() -> Path:
    return Path(__file__).resolve().parent / '_data_versions.yaml'


def get_latest_pipeline_versions() -> dict:
    with open(get_path_of_integration_version()) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def current_dataset_is_up_to_date(data_file: DataFile, dataset_path: str, latest_version: int) -> bool:
    return data_file.file[dataset_path].attrs['version'] == latest_version



def dataset_exists(data_file: DataFile, dataset_path: str) -> bool:
    try:
        data_file.file[dataset_path]
        return True
    except KeyError:
        return False
