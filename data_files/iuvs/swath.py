import warnings

import numpy as np

from pyuvs import minimum_mirror_angle, maximum_mirror_angle


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


def get_apoapse_swath_number(field_of_view: np.ndarray, orbit: int) -> np.ndarray:
    swath_number = compute_swath_number(field_of_view)
    if orbit in [3009, 3043]:
        swath_number += 1
    elif orbit in [3965]:
        swath_number += 4
    return swath_number


def get_number_of_swaths(swath_number: np.ndarray) -> np.ndarray:
    return np.array([swath_number[-1] + 1]) if swath_number.size > 0 else np.array([])


def get_apoapse_number_of_swaths(swath_number: np.ndarray, orbit: int) -> np.ndarray:
    number_of_swaths = get_number_of_swaths(swath_number)
    if orbit in [3115, 3174, 3211, 3229, 3248, 3375, 3488, 3688, 3692]:
        number_of_swaths += 1
    elif orbit in [3456, 3581]:
        number_of_swaths += 2
    elif orbit in [3721]:
        number_of_swaths += 3
    return number_of_swaths


def make_opportunity_classification(field_of_view: np.ndarray, swath_number: np.ndarray) -> np.ndarray:
    opportunity_integrations = np.empty(swath_number.shape, dtype='bool')
    for sn in np.unique(swath_number):
        angles = field_of_view[swath_number == sn]
        relay = convert_mirror_angles_to_field_of_view(minimum_mirror_angle) in angles and \
                convert_mirror_angles_to_field_of_view(maximum_mirror_angle) in angles
        opportunity_integrations[swath_number == sn] = relay
    return opportunity_integrations


def get_apoapse_opportunity_classification():
    pass
