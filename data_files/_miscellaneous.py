import typing

from astropy.io import fits
import h5py
import numpy as np

from _data_versions import get_latest_pipeline_versions, dataset_exists, current_dataset_is_up_to_date


hdulist: typing.TypeAlias = fits.hdu.hdulist.HDUList


def get_opportunity_file_indices(file: h5py.File, integration_path: str):
    opportunity_integrations = file[f'{integration_path}/opportunity'][:]
    data_file = file[f'{integration_path}/data_file'][:]
    return np.unique(data_file[opportunity_integrations])


def add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
    return array if np.ndim(array) == expected_dims else array[None, :]


def get_integrations_per_file(hduls: list[hdulist]) -> list[int]:
    return [add_dimension_if_necessary(f['primary'].data, 3).shape[0] for f in hduls]


def add_data_to_file(file: h5py.File, get_data: callable, dataset_name: str, group_path: str, unit: str, comment: str,
                     dataset_version_name: str = None, compression='gzip', compression_opts=4):
    dataset_version_name = f'{dataset_name}' if dataset_version_name is None else dataset_version_name
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment
