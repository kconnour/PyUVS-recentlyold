import h5py
import numpy as np

import pyuvs as pu


compression = 'gzip'
compression_opts = 4


def add_channel_dependent_integration_data_to_file(file: h5py.File, integration_path: str, hduls: pu.typing.hdulist) -> None:
    # TODO: it'd be nice to add pointers to the channel independent integration arrays, but h5py doesn't support that yet
    #  (there's currently a pull request)
    add_detector_temperature(file, integration_path, hduls)
    add_voltage(file, integration_path, hduls)
    add_voltage_gain(file, integration_path, hduls)
    add_failsafe_integrations(file, integration_path)
    add_dayside_integrations(file, integration_path)
    add_nightside_integrations(file, integration_path)


def add_detector_temperature(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'detector_temperature'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/det_temp_c structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_voltage(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = pu.file_classification.get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_volt'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'voltage'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Volts'
    comment = 'This data is taken from the observation/mcp_volt structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_voltage_gain(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = pu.file_classification.get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_gain'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'voltage_gain'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Volts'
    comment = 'This data is taken from the observation/mcp_gain structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_failsafe_integrations(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{group_path}/voltage'][:]
        return voltage == pu.constants.failsafe_voltage

    dataset_name = 'failsafe'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration was not part of normal science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_dayside_integrations(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{group_path}/voltage'][:]
        return np.logical_and(voltage < pu.constants.day_night_voltage_boundary, voltage != pu.constants.failsafe_voltage)

    dataset_name = 'dayside'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration was part of dayside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_nightside_integrations(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{group_path}/voltage'][:]
        return voltage > pu.constants.day_night_voltage_boundary

    dataset_name = 'nightside'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration was part of nightside science; False otherwise. ' \
              'Derived from engineering settings of observation/mcp_gain structure of v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
