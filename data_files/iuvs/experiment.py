import numpy as np

from pyuvs import apoapse_muv_failsafe_voltage, apoapse_muv_day_night_voltage_boundary


def apoapse_muv_failsafe_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    return np.isclose(mcp_voltage, apoapse_muv_failsafe_voltage)


def apoapse_muv_dayside_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    failsafe_integrations = apoapse_muv_failsafe_integrations(mcp_voltage)
    nightside_integrations = apoapse_muv_nightside_integrations(mcp_voltage)
    return ~(failsafe_integrations + nightside_integrations).astype('bool')


def apoapse_muv_nightside_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    return mcp_voltage > apoapse_muv_day_night_voltage_boundary
