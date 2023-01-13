import numpy as np

from _structure import DataFile
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, hdulist


def add_sub_spacecraft_latitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls])

    dataset_name = 'sub_spacecraft_latitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lat structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_spacecraft_longitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls])

    dataset_name = 'sub_spacecraft_longitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lon structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_solar_latitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls])

    dataset_name = 'sub_solar_latitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lat structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_solar_longitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls])

    dataset_name = 'sub_solar_longitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lon structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_spacecraft_altitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls])

    dataset_name = 'sub_spacecraft_altitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'km'
    comment = 'This data is taken from the spacecraftgeometry/spacecraft_alt structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_instrument_sun_angle(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls])

    dataset_name = 'instrument_sun_angle'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees'
    comment = 'This data is taken from the spacecraftgeometry/inst_sun_angle structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_spacecraft_velocity_inertial_frame(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.vstack([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls])

    dataset_name = 'spacecraft_velocity_inertial_frame'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'km/s'
    comment = 'This data is taken from the spacecraftgeometry/v_spacecraft_rate_inertial structure of the v13 IUVS data.' \
              'This is the spacecraft velocity relative to Mars\' center of mass in the inertial frame.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_instrument_x_field_of_view(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.vstack([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls])

    dataset_name = 'instrument_x_field_of_view'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Unit vector'
    comment = 'This data is taken from the spacecraftgeometry/vx_instrument_inertial structure of the v13 IUVS data.' \
              'It is the direction of the instrument field of view X axis, including scan mirror rotation (i.e. the ' \
              'instrument spatial direction).'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_app_flip(data_file: DataFile, group_path: str) -> None:
    def get_data() -> np.ndarray:
        vx = data_file.file[f'{group_path}/instrument_x_field_of_view'][:][:, 0]
        sc_rate = data_file.file[f'{group_path}/spacecraft_velocity_inertial_frame'][:][:, 0]
        dot = vx * sc_rate > 0
        return np.array([np.mean(dot) >= 0.5])

    dataset_name = 'app_flip'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    comment = 'True if the APP is flipped; False otherwise. This is derived from v13 of the IUVS data. ' \
              'It is the average of the dot product between the instrument direction and the spacecraft velocity.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
