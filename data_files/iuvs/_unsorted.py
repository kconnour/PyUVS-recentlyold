import numpy as np


def convert_mirror_angles_to_field_of_view(mirror_angles: np.ndarray) -> np.ndarray:
    return mirror_angles * 2


def convert_mcp_voltage_data_number_to_volts(data_number: np.ndarray) -> np.ndarray:
    # Note that I don't know where data number is in our data images but this creates the MCP volt structure
    return 0.244 * data_number - 1.83
