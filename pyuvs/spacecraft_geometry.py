import numpy as np

from pyuvs.typing import hdulist
from pyuvs.constants import latest_hdul_file_version


def get_subsolar_latitude_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls]) if hduls else np.array([])


def get_subsolar_longitude_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls]) if hduls else np.array([])


def get_subspacecraft_latitude_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls]) if hduls else np.array([])


def get_subspacecraft_longitude_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls]) if hduls else np.array([])


def get_subspacecraft_altitude_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls]) if hduls else np.array([])


def get_instrument_sun_angle_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls]) if hduls else np.array([])


def add_spacecraft_velocity_inertial_frame_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls]) if hduls else np.array([])


def get_instrument_x_field_of_view_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls]) if hduls else np.array([])


def compute_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0] > 0
        app_flip = np.array([np.mean(dot) >= 0.5])
    except IndexError:
        app_flip = np.array([])
    return app_flip

subsolar_latitude_hdul_comment: str = f'This data is taken from the spacecraftgeometry/sub_solar_lat structure of the version {latest_hdul_file_version} IUVS data.'
subsolar_longitude_hdul_comment: str = f'This data is taken from the spacecraftgeometry/sub_solar_lon structure of the version {latest_hdul_file_version} IUVS data.'
subspacecraft_latitude_hdul_comment: str = f'This data is taken from the spacecraftgeometry/sub_spacecraft_lat structure of the version {latest_hdul_file_version} IUVS data.'
subspacecraft_longitude_hdul_comment: str = f'This data is taken from the spacecraftgeometry/sub_subspacecraft_lon structure of the version {latest_hdul_file_version} IUVS data.'
subspacecraft_altitude_hdul_comment: str = f'This data is taken from the spacecraftgeometry/spacecraft_alt structure of the version {latest_hdul_file_version} IUVS data.'
instrument_sun_angle_hdul_comment: str = f'This data is taken from the spacecraftgeometry/inst_sun_angle structure of the version {latest_hdul_file_version} IUVS data.'
spacecraft_velocity_inertial_frame_comment: str = f'This data is taken from the spacecraftgeometry/v_spacecraft_rate_inertial structure of the version {latest_hdul_file_version} IUVS data.' \
              'This is the spacecraft velocity relative to Mars\' center of mass in the inertial frame.'
instrument_x_field_of_view_hdul_comment: str = f'This data is taken from the spacecraftgeometry/vx_instrument_inertial structure of the version {latest_hdul_file_version} IUVS data.' \
              'It is the direction of the instrument field of view X axis, including scan mirror rotation (i.e. the ' \
              'instrument spatial direction).'
app_flip_comment: str = 'True if the APP is flipped; False otherwise. This is derived from v13 of the IUVS data. ' \
              'It is the average of the dot product between the instrument direction and the spacecraft velocity.'
