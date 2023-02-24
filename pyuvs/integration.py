import warnings

import numpy as np

from pyuvs.typing import hdulist
from pyuvs.constants import latest_hdul_file_version, minimum_mirror_angle, maximum_mirror_angle
from pyuvs.file_classification import get_integrations_per_file


def get_ephemeris_time_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])


def get_field_of_view_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['fov_deg'] for f in hduls]) if hduls else np.array([])


def get_mirror_data_number_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls]) if hduls else np.array([])


def get_case_temperature_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls]) if hduls else np.array([])


def get_detector_temperature_from_hduls(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls]) if hduls else np.array([])


def get_integration_time_from_hduls(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['int_time'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


def get_data_file_number(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(c, integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


def get_mcp_voltage_from_hduls(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['mcp_volt'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


def get_mcp_voltage_gain_from_hduls(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['mcp_gain'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


def compute_swath_number(mirror_angles: np.ndarray) -> np.ndarray:
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


def make_opportunity_classification(field_of_view: np.ndarray, swath_number: np.ndarray) -> np.ndarray:
    relay_integrations = np.empty(swath_number.shape, dtype='bool')
    for sn in np.unique(swath_number):
        angles = field_of_view[swath_number == sn]
        relay = convert_mirror_angles_to_field_of_view(minimum_mirror_angle) in angles and \
                convert_mirror_angles_to_field_of_view(maximum_mirror_angle) in angles
        relay_integrations[swath_number == sn] = relay
    return relay_integrations


def convert_mirror_angles_to_field_of_view(mirror_angles: np.ndarray) -> np.ndarray:
    return mirror_angles * 2


def convert_mcp_voltage_data_number_to_volts(data_number: np.ndarray) -> np.ndarray:
    # Note that I don't know where data number is in our data images but this creates the MCP volt structure
    return 0.244 * data_number - 1.83


ephemeris_time_hdul_comment: str = f'This data is taken from the integration/et structure of the version {latest_hdul_file_version} IUVS data.'
field_of_view_hdul_comment: str = f'This data is taken from the integration/fov_deg structure of the version {latest_hdul_file_version} IUVS data.'
mirror_data_number_hdul_comment: str = f'This data is taken from the integration/mirror_dn structure of the version {latest_hdul_file_version} IUVS data.'
case_temperature_hdul_comment: str = f'This data is taken from the integration/case_temp_c structure of the version {latest_hdul_file_version} IUVS data.'
detector_temperature_hdul_comment: str = f'This data is taken from the integration/det_temp_c structure of the version {latest_hdul_file_version} IUVS data.'
integration_time_hdul_comment: str = f'This data is from the observation/int_time structure of the version {latest_hdul_file_version} IUVS data.'
mcp_voltage_hdul_comment: str = f'This data is taken from the observation/mcp_volt structure of the version {latest_hdul_file_version} IUVS data.'
mcp_voltage_gain_hdul_comment: str = f'This data is taken from the observation/mcp_gain structure of the version {latest_hdul_file_version} IUVS data.'
data_file_comment: str = 'This is the file index corresponding to each integration.'
