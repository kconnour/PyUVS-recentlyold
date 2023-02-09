import numpy as np

from pyuvs.typing import hdulist
from pyuvs.constants import apoapse_muv_day_night_voltage_boundary
from pyuvs.failsafe import get_apoapse_muv_failsafe_voltage


def add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
    return array if np.ndim(array) == expected_dims else array[None, :]


def get_integrations_per_file(hduls: hdulist) -> list[int]:
    return [add_dimension_if_necessary(f['primary'].data, 3).shape[0] for f in hduls]


def determine_apoapse_muv_dayside_files(hduls: hdulist) -> np.ndarray:
    return np.array([f['observation'].data['mcp_volt'][0] < apoapse_muv_day_night_voltage_boundary for f in hduls])


def determine_apoapse_muv_failsafe_files(hduls: hdulist, orbit: int) -> np.ndarray:
    # This is horseshit that I can't check for equality. Numpy assures me these values are not equal despite being
    # equal with maximum numeric resolution
    voltage = get_apoapse_muv_failsafe_voltage(orbit)
    return np.array([np.isclose(f['observation'].data['mcp_volt'][0], voltage) for f in hduls])
