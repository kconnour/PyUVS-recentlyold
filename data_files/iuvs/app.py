import numpy as np


def compute_apoapse_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0] > 0
        app_flip = np.array([np.mean(dot) >= 0.2])
    except IndexError:
        app_flip = np.array([])
    return app_flip
