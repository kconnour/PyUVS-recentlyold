import h5py
import numpy as np

from pyuvs.typing import hdulist
from pyuvs.data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists


compression = 'gzip'
compression_opts = 4


def add_spacecraft_geometry_data_to_file(file: h5py.File, spacecraft_geometry_path: str, segment_path: str, hduls: hdulist) -> None:
    add_subsolar_latitude(file, spacecraft_geometry_path, hduls)
    add_subsolar_longitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_latitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_longitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_altitude(file, spacecraft_geometry_path, hduls)
    add_instrument_sun_angle(file, spacecraft_geometry_path, hduls)
    add_spacecraft_velocity_inertial_frame(file, spacecraft_geometry_path, hduls)
    add_instrument_x_field_of_view(file, spacecraft_geometry_path, hduls)
    add_app_flip(file, spacecraft_geometry_path, segment_path)


def add_subsolar_latitude(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subsolar_latitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lat structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_subsolar_longitude(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subsolar_longitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lon structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_subspacecraft_latitude(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_latitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lat structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_subspacecraft_longitude(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_longitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lon structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_subspacecraft_altitude(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_altitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km'
    comment = 'This data is taken from the spacecraftgeometry/spacecraft_alt structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_instrument_sun_angle(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'instrument_sun_angle'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the spacecraftgeometry/inst_sun_angle structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_spacecraft_velocity_inertial_frame(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'spacecraft_velocity_inertial_frame'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km/s'
    comment = 'This data is taken from the spacecraftgeometry/v_spacecraft_rate_inertial structure of the v13 IUVS data.' \
              'This is the spacecraft velocity relative to Mars\' center of mass in the inertial frame.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_instrument_x_field_of_view(file: h5py.File, group_path: str, hduls: hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'instrument_x_field_of_view'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Unit vector'
    comment = 'This data is taken from the spacecraftgeometry/vx_instrument_inertial structure of the v13 IUVS data.' \
              'It is the direction of the instrument field of view X axis, including scan mirror rotation (i.e. the ' \
              'instrument spatial direction).'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_app_flip(file: h5py.File, group_path: str, segment_path: str) -> None:
    def get_data() -> np.ndarray:
        try:
            vx = file[f'{group_path}/instrument_x_field_of_view'][:][:, 0]
            sc_rate = file[f'{group_path}/spacecraft_velocity_inertial_frame'][:][:, 0]
            dot = vx * sc_rate > 0
            app_flip =  np.array([np.mean(dot) >= 0.5])
        except IndexError:
            app_flip = np.array([])
        return app_flip

    dataset_name = 'app_flip'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{segment_path}/{dataset_name}'
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the APP is flipped; False otherwise. This is derived from v13 of the IUVS data. ' \
              'It is the average of the dot product between the instrument direction and the spacecraft velocity.'

    if not dataset_exists(file, dataset_path):
        dataset = file[segment_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[segment_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
