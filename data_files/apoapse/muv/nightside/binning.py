import h5py
import numpy as np

import pyuvs as pu


group_path = 'apoapse/muv/nightside/binning'


def add_binning_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_spatial_bin_edges(file, hduls)
    add_spectral_bin_edges(file, hduls)


def add_spatial_bin_edges(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.binning.get_spatial_bin_edges_from_hduls(hduls)

    dataset_name = 'spatial_bin_edges'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = pu.binning.spatial_bin_edges_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        bin_edges = get_data()
        dataset = file[group_path].create_dataset(dataset_name, data=bin_edges, compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        bin_edges = get_data()
        dataset[:] = bin_edges
        dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_spectral_bin_edges(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.binning.get_spectral_bin_edges_from_hduls(hduls)

    dataset_name = 'spectral_bin_edges'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = pu.binning.spectral_bin_edges_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        bin_edges = get_data()
        dataset = file[group_path].create_dataset(dataset_name, data=bin_edges, compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        bin_edges = get_data()
        dataset[:] = bin_edges
        dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
