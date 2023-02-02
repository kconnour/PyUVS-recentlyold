import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/spacecraft_geometry'


def add_spacecraft_geometry_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_subsolar_latitude(file, hduls)
    add_subsolar_longitude(file, hduls)
    add_subspacecraft_latitude(file, hduls)
    add_subspacecraft_longitude(file, hduls)
    add_subspacecraft_altitude(file, hduls)
    add_instrument_sun_angle(file, hduls)
    add_spacecraft_velocity_inertial_frame(file, hduls)
    add_instrument_x_field_of_view(file, hduls)
    add_app_flip(file)


def add_subsolar_latitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subsolar_latitude_from_hduls(hduls)

    dataset_name = 'subsolar_latitude'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.latitude
    comment = pu.spacecraft_geometry.subsolar_latitude_hdul_comment

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


def add_subsolar_longitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subsolar_longitude_from_hduls(hduls)

    dataset_name = 'subsolar_longitude'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.longitude
    comment = pu.spacecraft_geometry.subsolar_longitude_hdul_comment

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


def add_subspacecraft_latitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_latitude_from_hduls(hduls)

    dataset_name = 'subspacecraft_latitude'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.latitude
    comment = pu.spacecraft_geometry.subspacecraft_latitude_hdul_comment

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


def add_subspacecraft_longitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_longitude_from_hduls(hduls)

    dataset_name = 'subspacecraft_longitude'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.longitude
    comment = pu.spacecraft_geometry.subspacecraft_longitude_hdul_comment

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


def add_subspacecraft_altitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_altitude_from_hduls(hduls)

    dataset_name = 'subspacecraft_altitude'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.altitude
    comment = pu.spacecraft_geometry.subspacecraft_altitude_hdul_comment

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


def add_instrument_sun_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_instrument_sun_angle_from_hduls(hduls)

    dataset_name = 'instrument_sun_angle'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.instrument_sun_angle
    comment = pu.spacecraft_geometry.instrument_sun_angle_hdul_comment

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


def add_spacecraft_velocity_inertial_frame(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.add_spacecraft_velocity_inertial_frame_from_hduls(hduls)

    dataset_name = 'spacecraft_velocity_inertial_frame'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = pu.units.velocity
    comment = pu.spacecraft_geometry.spacecraft_velocity_inertial_frame_comment

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


def add_instrument_x_field_of_view(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_instrument_x_field_of_view_from_hduls(hduls)

    dataset_name = 'instrument_x_field_of_view'
    dataset_path = f'{path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_path]
    unit = pu.units.unit_vector
    comment = pu.spacecraft_geometry.instrument_x_field_of_view_hdul_comment

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


def add_app_flip(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        vx = file[f'{path}/instrument_x_field_of_view'][:]
        sc_rate = file[f'{path}/spacecraft_velocity_inertial_frame'][:]
        return pu.spacecraft_geometry.compute_app_flip(vx, sc_rate)

    segment_path = 'apoapse'
    dataset_name = 'app_flip'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{segment_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = pu.spacecraft_geometry.app_flip_comment

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[segment_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[segment_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
