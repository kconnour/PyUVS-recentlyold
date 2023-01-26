import h5py
import numpy as np

from _miscellaneous import hdulist, add_data_to_file


def add_spacecraft_geometry_data_to_file(file: h5py.File, spacecraft_geometry_path: str, segment_path: str, hduls: list[hdulist]) -> None:
    file.require_group(spacecraft_geometry_path)
    add_subsolar_latitude(file, spacecraft_geometry_path, hduls)
    add_subsolar_longitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_latitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_longitude(file, spacecraft_geometry_path, hduls)
    add_subspacecraft_altitude(file, spacecraft_geometry_path, hduls)
    add_instrument_sun_angle(file, spacecraft_geometry_path, hduls)
    add_spacecraft_velocity_inertial_frame(file, spacecraft_geometry_path, hduls)
    add_instrument_x_field_of_view(file, spacecraft_geometry_path, hduls)
    add_app_flip(file, spacecraft_geometry_path, segment_path)


def add_subsolar_latitude(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subsolar_latitude'
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lat structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_subsolar_longitude(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subsolar_longitude'
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_solar_lon structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_subspacecraft_latitude(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_latitude'
    unit = 'Degrees [N]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lat structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_subspacecraft_longitude(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_longitude'
    unit = 'Degrees [E]'
    comment = 'This data is taken from the spacecraftgeometry/sub_spacecraft_lon structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_subspacecraft_altitude(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'subspacecraft_altitude'
    unit = 'km'
    comment = 'This data is taken from the spacecraftgeometry/spacecraft_alt structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_instrument_sun_angle(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'instrument_sun_angle'
    unit = 'Degrees'
    comment = 'This data is taken from the spacecraftgeometry/inst_sun_angle structure of the v13 IUVS data.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_spacecraft_velocity_inertial_frame(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'spacecraft_velocity_inertial_frame'
    unit = 'km/s'
    comment = 'This data is taken from the spacecraftgeometry/v_spacecraft_rate_inertial structure of the v13 IUVS data.' \
              'This is the spacecraft velocity relative to Mars\' center of mass in the inertial frame.'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


def add_instrument_x_field_of_view(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'instrument_x_field_of_view'
    unit = 'Unit vector'
    comment = 'This data is taken from the spacecraftgeometry/vx_instrument_inertial structure of the v13 IUVS data.' \
              'It is the direction of the instrument field of view X axis, including scan mirror rotation (i.e. the ' \
              'instrument spatial direction).'
    add_data_to_file(file, get_data, dataset_name, group_path, unit, comment)


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
    unit = ''
    comment = 'True if the APP is flipped; False otherwise. This is derived from v13 of the IUVS data. ' \
              'It is the average of the dot product between the instrument direction and the spacecraft velocity.' \
              'I assume a single APP orientation per orbit.'
    add_data_to_file(file, get_data, dataset_name, segment_path, unit, comment)
