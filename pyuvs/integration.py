import warnings

import numpy as np

from pyuvs.typing import hdulist
from pyuvs.constants import latest_hdul_file_version, minimum_mirror_angle, maximum_mirror_angle
from pyuvs.file_classification import get_integrations_per_file


def get_ephemeris_time_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])


ephemeris_time_unit: str = 'Seconds since J2000'
ephemeris_time_hdul_comment: str = f'This data is taken from the integration/et structure of the version {latest_hdul_file_version} IUVS data.'


def get_field_of_view_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['fov_deg'] for f in hduls]) if hduls else np.array([])


field_of_view_unit: str = 'Degrees'
field_of_view_hdul_comment: str = f'This data is taken from the integration/fov_deg structure of the version {latest_hdul_file_version} IUVS data.'


def convert_mirror_angles_to_field_of_view(mirror_angles: np.ndarray) -> np.ndarray:
    return mirror_angles * 2


def get_mirror_data_number_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls]) if hduls else np.array([])


mirror_data_number_unit = 'DN'
mirror_data_number_hdul_comment: str = f'This data is taken from the integration/mirror_dn structure of the version {latest_hdul_file_version} IUVS data.'


def get_case_temperature_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls]) if hduls else np.array([])


case_temperature_unit = 'Degrees C'
case_temperature_hdul_comment: str = f'This data is taken from the integration/case_temp_c structure of the version {latest_hdul_file_version} IUVS data.'


def get_integration_time_from_hduls(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['int_time'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


integration_time_unit: str = 'Seconds'
integration_time_hdul_comment: str = f'This data is from the observation/int_time structure of the version {latest_hdul_file_version} IUVS data.'


def get_data_file_number(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(c, integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


data_file_comment: str = 'This is the file index corresponding to each integration.'


def make_swath_number(mirror_angles: np.ndarray) -> np.ndarray:
    """Make the swath number associated with each mirror angle.

    This function assumes the input is all the mirror angles (or, equivalently,
    the field of view) from an orbital segment. Omitting some mirror angles
    may result in nonsensical results. Adding additional mirror angles from
    multiple segments or orbits will certainly result in nonsensical results.

    Returns
    -------
    np.ndarray
        The swath number associated with each mirror angle.

    Notes
    -----
    This algorithm assumes the mirror in roughly constant step sizes except
    when making a swath jump. It finds the median step size and then uses
    this number to find swath discontinuities. It interpolates between these
    indices and takes the floor of these values to get the integer swath
    number.

    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mirror_change = np.diff(mirror_angles)
        threshold = np.abs(np.median(mirror_change)) * 4
        mirror_discontinuities = np.where(np.abs(mirror_change) > threshold)[0] + 1
        if any(mirror_discontinuities):
            n_swaths = len(mirror_discontinuities) + 1
            integrations = range(len(mirror_angles))
            interp_swaths = np.interp(integrations, mirror_discontinuities, range(1, n_swaths), left=0)
            return np.floor(interp_swaths).astype('int')
        else:
            return np.zeros(mirror_angles.shape)


swath_number_comment: str = 'The swath number corresponding to each integration.'


def make_opportunity_classification(field_of_view: np.ndarray, swath_number: np.ndarray) -> np.ndarray:
    relay_integrations = np.empty(swath_number.shape, dtype='bool')
    for sn in np.unique(swath_number):
        angles = field_of_view[swath_number == sn]
        relay = convert_mirror_angles_to_field_of_view(minimum_mirror_angle) in angles and \
                convert_mirror_angles_to_field_of_view(maximum_mirror_angle) in angles
        relay_integrations[swath_number == sn] = relay
    return relay_integrations


opportunity_classification_comment: str = 'True if the integration is part of a opportunistic swath; False otherwise.'
