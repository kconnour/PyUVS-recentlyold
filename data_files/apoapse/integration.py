import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/integration'


def add_channel_independent_integration_data_to_file(file: h5py.File, hduls: pu.typing.hdulist, orbit: int) -> None:
    add_ephemeris_time(file, hduls)
    add_field_of_view(file, hduls)
    add_mirror_data_number(file, hduls)
    add_case_temperature(file, hduls)
    add_integration_time(file, hduls)
    add_data_file(file, hduls)
    add_swath_number(file, orbit)
    add_opportunity_classification(file)
    add_number_of_swaths(file, orbit)


def add_ephemeris_time(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_ephemeris_time_from_hduls(hduls)

    dataset = file[path].create_dataset('ephemeris_time', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.ephemeris_time
    dataset.attrs['comment'] = pu.integration.ephemeris_time_hdul_comment


def add_field_of_view(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_field_of_view_from_hduls(hduls)

    dataset = file[path].create_dataset('field_of_view', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.field_of_view
    dataset.attrs['comment'] = pu.integration.field_of_view_hdul_comment


def add_mirror_data_number(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mirror_data_number_from_hduls(hduls)

    dataset = file[path].create_dataset('mirror_data_number', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = pu.integration.mirror_data_number_hdul_comment


def add_case_temperature(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_case_temperature_from_hduls(hduls)

    dataset = file[path].create_dataset('case_temperature', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.temperature
    dataset.attrs['comment'] = pu.integration.case_temperature_hdul_comment


def add_integration_time(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_integration_time_from_hduls(hduls)

    dataset = file[path].create_dataset('integration_time', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.integration_time
    dataset.attrs['comment'] = pu.integration.integration_time_hdul_comment


def add_data_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_data_file_number(hduls)

    dataset = file[path].create_dataset('data_file', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = pu.integration.data_file_comment


def add_swath_number(file: h5py.File, orbit: int) -> None:
    def get_data() -> np.ndarray:
        field_of_view = file[f'{path}/field_of_view'][:]
        swath_numbers = pu.integration.compute_swath_number(field_of_view)

        if orbit == 239:
            swath_numbers += 1

        return swath_numbers

    dataset = file[path].create_dataset('swath_number', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'The swath number of each integration, modified to account for apoapse oddities.'


def add_opportunity_classification(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        field_of_view = file[f'{path}/field_of_view'][:]
        swath_number = file[f'{path}/swath_number'][:]
        return pu.integration.make_opportunity_classification(field_of_view, swath_number)

    dataset = file[path].create_dataset('opportunity', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'True if an opportunistic observation; False otherwise.'


def add_number_of_swaths(file: h5py.File, orbit: int) -> None:
    def get_data() -> np.ndarray:
        swath_number = file[f'{path}/swath_number'][:]
        if swath_number.size == 0:
            return np.array([0])
        else:
            return np.array([swath_number[-1] + 1])

    dataset = file[path].create_dataset('n_swaths', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'The number of swaths intended for this observation sequence (not necessarily the number of swaths taken)'
