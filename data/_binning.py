import warnings

import h5py
import numpy as np

from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, hdulist


def add_spatial_bin_edges(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        # All files should have the same spatial binning, so just get the first file's info
        return np.append(hduls[0]['binning'].data['spapixlo'][0], hduls[0]['binning'].data['spapixhi'][0, -1] + 1) if hduls else np.array([])

    def get_bin_width(edges: np.ndarray):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=RuntimeWarning)
                width = int(np.median(np.diff(edges)))
        except ValueError:
            width = 0
        return width

    dataset_name = 'spatial_bin_edges'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'bin number'
    comment = 'This data is taken from the binning/spapixlo and spapixhi structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        bin_edges = get_data()
        dataset = file[group_path].create_dataset(dataset_name, data=bin_edges)
        dataset.attrs['width'] = get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        bin_edges = get_data()
        dataset[:] = bin_edges
        dataset.attrs['width'] = get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_spectral_bin_edges(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        # All files should have the same spatial binning, so just get the first file's info
        return np.append(hduls[0]['binning'].data['spepixlo'][0], hduls[0]['binning'].data['spepixhi'][0, -1] + 1) if hduls else np.array([])

    def get_bin_width(edges: np.ndarray):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=RuntimeWarning)
                width = int(np.median(np.diff(edges)))
        except ValueError:
            width = 0
        return width

    dataset_name = 'spectral_bin_edges'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'bin number'
    comment = 'This data is taken from the binning/spepixlo and spepixhi structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        bin_edges = get_data()
        dataset = file[group_path].create_dataset(dataset_name, data=bin_edges)
        dataset.attrs['width'] = get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        bin_edges = get_data()
        dataset[:] = bin_edges
        dataset.attrs['width'] = get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment
