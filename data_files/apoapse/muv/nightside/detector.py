import h5py
import numpy as np

import pyuvs as pu


group_path = 'apoapse/muv/nightside/detector'


def add_detector_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_raw(file, hduls)
    add_dark_subtracted(file, hduls)
    add_brightness(file)


def get_app_flip(file: h5py.File) -> bool:
    return file[f'apoapse/app_flip'][:]


def add_raw(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.detector.get_raw_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('raw', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.dn
    dataset.attrs['comment'] = pu.detector.raw_hdul_comment


def add_dark_subtracted(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.detector.get_dark_subtracted_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('dark_subtracted', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.dn
    dataset.attrs['comment'] = pu.detector.dark_subtracted_hdul_comment


def add_brightness(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        dark_subtracted = file[f'{group_path}/dark_subtracted'][:]
        spatial_bin_edges_ds = file[f'/apoapse/muv/nightside/binning/spatial_bin_edges']
        spatial_bin_edges = spatial_bin_edges_ds[:]
        spatial_bin_width = spatial_bin_edges_ds.attrs['width']
        spectral_bin_edges_ds = file[f'/apoapse/muv/nightside/binning/spectral_bin_edges']
        spectral_bin_edges = spectral_bin_edges_ds[:]
        spectral_bin_width = spectral_bin_edges_ds.attrs['width']

        good_integrations = file['apoapse/muv/integration/nightside'][:]
        integration_time = file[f'apoapse/integration/integration_time'][:][good_integrations]
        voltage = file[f'apoapse/muv/integration/mcp_voltage'][:][good_integrations]
        voltage_gain = file[f'apoapse/muv/integration/mcp_voltage_gain'][:][good_integrations]

        app = get_app_flip(file)
        return pu.detector.make_brightness(dark_subtracted, spatial_bin_edges, spatial_bin_width, spectral_bin_edges, spectral_bin_width,
                                           integration_time, voltage, voltage_gain, app)

    dataset = file[group_path].create_dataset('brightness', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.brightness
    dataset.attrs['comment'] = pu.detector.brightness_comment
