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

    dataset_name = 'detector_temperature'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.temperature
    comment = pu.integration.detector_temperature_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mcp_voltage(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mcp_voltage_from_hduls(hduls)

    dataset_name = 'mcp_voltage'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.voltage
    comment = pu.integration.mcp_voltage_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mcp_voltage_gain(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mcp_voltage_gain_from_hduls(hduls)

    dataset_name = 'mcp_voltage_gain'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.voltage
    comment = pu.integration.mcp_voltage_gain_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_failsafe_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return voltage == pu.constants.apoapse_muv_failsafe_voltage

    dataset_name = 'failsafe'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = 'True if the integration was taken during a failsafe observation; False otherwise.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_dayside_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return np.logical_and(voltage < pu.constants.apoapse_muv_day_night_voltage_boundary, voltage != pu.constants.apoapse_muv_failsafe_voltage)

    dataset_name = 'dayside'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration was part of dayside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_nightside_integrations(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{path}/mcp_voltage'][:]
        return voltage > pu.constants.apoapse_muv_day_night_voltage_boundary

    dataset_name = 'nightside'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration was part of nightside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
