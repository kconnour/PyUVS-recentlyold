import numpy as np

from pyuvs.constants import latest_hdul_file_version
from pyuvs.file_classification import add_dimension_if_necessary
from pyuvs.typing import hdulist


def get_latitude_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_lat'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_longitude_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_lon'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_tangent_altitude_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_tangent_altitude_rate_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt_rate'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_line_of_sight_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_los'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_solar_zenith_angle_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_solar_zenith_angle'], 2) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_emission_angle_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_emission_angle'], 2) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_phase_angle_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_phase_angle'], 2) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_zenith_angle_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_zenith_angle'], 2) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_local_time_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_local_time'], 2) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_right_ascension_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_ra'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_declination_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_dec'], 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_bin_vector_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([np.moveaxis(add_dimension_if_necessary(f['pixelgeometry'].data['pixel_vec'], 4), 1, -1) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


latitude_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_lat structure of the version {latest_hdul_file_version} IUVS data.'
longitude_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_lon structure of the version {latest_hdul_file_version} IUVS data.'
tangent_altitude_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_mrh_alt structure of the version {latest_hdul_file_version} IUVS data.'
tangent_altitude_rate_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_mrh_alt_rate structure of the version {latest_hdul_file_version} IUVS data.'
line_of_sight_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_los structure of the version {latest_hdul_file_version} IUVS data.'
solar_zenith_angle_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_solar_zenith_angle structure of the version {latest_hdul_file_version} IUVS data.'
emission_angle_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_emission_angle structure of the version {latest_hdul_file_version} IUVS data.'
phase_angle_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_phase_angle structure of the version {latest_hdul_file_version} IUVS data.'
zenith_angle_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_zenith_angle structure of the version {latest_hdul_file_version} IUVS data.'
local_time_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_local_time structure of the version {latest_hdul_file_version} IUVS data.'
right_ascension_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_ra structure of the version {latest_hdul_file_version} IUVS data.'
declination_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_corner_dec structure of the version {latest_hdul_file_version} IUVS data.'
bin_vector_hdul_comment: str = f'This data is taken from the pixelgeometry/pixel_vec structure of the version {latest_hdul_file_version} IUVS data.'
