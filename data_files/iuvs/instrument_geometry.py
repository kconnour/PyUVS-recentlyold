from astropy.io import fits
import numpy as np

import iuvs_fits


@iuvs_fits.catch_empty_arrays
def make_instrument_x_field_of_view(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_x_field_of_view(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_instrument_sun_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_sun_angle(f) for f in hduls])


def compute_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0]
        app_flip = np.array([np.sum(dot) > 0])
    except ValueError:
        app_flip = np.array([])
    return app_flip
