import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/integration'


def add_channel_independent_integration_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_ephemeris_time(file, hduls)
    add_field_of_view(file, hduls)
    add_mirror_data_number(file, hduls)
    add_case_temperature(file, hduls)
    add_integration_time(file, hduls)
    add_data_file(file, hduls)
    add_swath_number(file)
    add_opportunity_classification(file)


def add_ephemeris_time(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_ephemeris_time_from_hduls(hduls)

    dataset_name = 'ephemeris_time'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.ephemeris_time
    comment = pu.integration.ephemeris_time_hdul_comment

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


def add_field_of_view(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_field_of_view_from_hduls(hduls)

    dataset_name = 'field_of_view'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.field_of_view
    comment = pu.integration.field_of_view_hdul_comment

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


def add_mirror_data_number(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_mirror_data_number_from_hduls(hduls)

    dataset_name = 'mirror_data_number'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = pu.integration.mirror_data_number_hdul_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_case_temperature(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_case_temperature_from_hduls(hduls)

    dataset_name = 'case_temperature'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.temperature
    comment = pu.integration.case_temperature_hdul_comment

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


def add_integration_time(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_integration_time_from_hduls(hduls)

    dataset_name = 'integration_time'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.integration_time
    comment = pu.integration.integration_time_hdul_comment

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


def add_data_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.integration.get_data_file_number(hduls)

    dataset_name = 'data_file'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = pu.integration.data_file_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_swath_number(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        field_of_view = file[f'{path}/field_of_view'][:]
        default_swath_numbers = pu.integration.compute_swath_number(field_of_view)
        return default_swath_numbers

    dataset_name = 'swath_number'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = 'The swath number of each integration, modified to account for apoapse oddities.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_opportunity_classification(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        field_of_view = file[f'{path}/field_of_view'][:]
        swath_number = file[f'{path}/swath_number'][:]
        return pu.integration.make_opportunity_classification(field_of_view, swath_number)

    dataset_name = 'opportunity'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    comment = 'True if an opportunistic observation; False otherwise.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[path].create_dataset(dataset_name, data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
