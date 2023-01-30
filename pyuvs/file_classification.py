import numpy as np

from pyuvs.typing import hdulist
from pyuvs.constants import day_night_voltage_boundary, failsafe_voltage


def add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
    return array if np.ndim(array) == expected_dims else array[None, :]


def get_integrations_per_file(hduls: hdulist) -> list[int]:
    return [add_dimension_if_necessary(f['primary'].data, 3).shape[0] for f in hduls]


def determine_dayside_files(hduls: hdulist) -> np.ndarray:
    return np.array([f['observation'].data['mcp_volt'][0] < day_night_voltage_boundary for f in hduls])


def determine_failsafe_files(hduls: hdulist) -> np.ndarray:
    # This is horseshit that I can't check for equality. Numpy assures me these values are not equal despite being
    # equal with maximum numeric resolution
    return np.array([np.isclose(f['observation'].data['mcp_volt'][0], failsafe_voltage) for f in hduls])
