from pathlib import Path

import yaml

from structure import DataFile


def get_path_of_integration_version() -> Path:
    return Path(__file__).resolve().parent / '_data_versions.yaml'


def get_latest_pipeline_versions() -> dict:
    with open(get_path_of_integration_version()) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def current_file_is_up_to_date(data_file: DataFile, dataset_path: str) -> bool:
    latest_pipeline_versions = get_latest_pipeline_versions()
    pipeline = dataset_path.split('/')[-1]
    try:
        return data_file.file[dataset_path].attrs['version'] == latest_pipeline_versions[pipeline]
    except KeyError:
        return False
