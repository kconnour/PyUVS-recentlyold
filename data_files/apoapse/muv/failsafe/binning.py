import h5py
import numpy as np

import pyuvs as pu


group_path = 'apoapse/muv/failsafe/binning'


def add_binning_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_spatial_bin_edges(file, hduls)
    add_spectral_bin_edges(file, hduls)


def add_spatial_bin_edges(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.binning.get_spatial_bin_edges_from_hduls(hduls)

    bin_edges = get_data()
    dataset = file[group_path].create_dataset('spatial_bin_edges', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
    dataset.attrs['comment'] = pu.binning.spatial_bin_edges_hdul_comment


def add_spectral_bin_edges(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.binning.get_spectral_bin_edges_from_hduls(hduls)

    bin_edges = get_data()
    dataset = file[group_path].create_dataset('spectral_bin_edges', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['width'] = pu.binning.get_bin_width(bin_edges)
    dataset.attrs['comment'] = pu.binning.spatial_bin_edges_hdul_comment
