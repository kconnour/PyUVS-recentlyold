import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/muv/integration'


def add_channel_dependent_integration_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    # TODO: it'd be nice to add pointers to the channel independent integration arrays, but h5py doesn't support that yet
    #  (there's currently a pull request)
    add_detector_temperature(file, hduls)
    add_mcp_voltage(file, hduls)
    add_mcp_voltage_gain(file, hduls)
    add_failsafe_integrations(file)
    add_dayside_integrations(file)
    add_nightside_integrations(file)


def add_detector_temperature(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_detector_temperature_from_hduls(hduls)

    dataset = file[path].create_dataset('detector_temperature', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.temperature
    dataset.attrs['comment'] = pu.integration.detector_temperature_hdul_comment


def add_mcp_voltage(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mcp_voltage_from_hduls(hduls)

    dataset = file[path].create_dataset('mcp_voltage', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.voltage
    dataset.attrs['comment'] = pu.integration.mcp_voltage_hdul_comment


def add_mcp_voltage_gain(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mcp_voltage_gain_from_hduls(hduls)

    dataset = file[path].create_dataset('mcp_voltage_gain', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.voltage
    dataset.attrs['comment'] = pu.integration.mcp_voltage_gain_hdul_comment


def add_failsafe_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return voltage == pu.constants.apoapse_muv_failsafe_voltage

    dataset = file[path].create_dataset('failsafe', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'True if the integration was taken during a failsafe observation; False otherwise.'


def add_dayside_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return np.logical_and(voltage < pu.constants.apoapse_muv_day_night_voltage_boundary, voltage != pu.constants.apoapse_muv_failsafe_voltage)

    dataset = file[path].create_dataset('dayside', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'True if the integration was part of dayside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'


def add_nightside_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return voltage > pu.constants.apoapse_muv_day_night_voltage_boundary

    dataset = file[path].create_dataset('nightside', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = 'True if the integration was part of nightside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'
