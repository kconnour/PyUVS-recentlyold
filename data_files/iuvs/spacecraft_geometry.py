from astropy.io import fits
import numpy as np

import iuvs_fits


@iuvs_fits.catch_empty_arrays
def make_subsolar_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_latitude(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_subsolar_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_longitude(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_subspacecraft_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_latitude(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_subspacecraft_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_longitude(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_subspacecraft_altitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_altitude(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_spacecraft_velocity_inertial_frame(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_spacecraft_velocity_inertial_frame(f) for f in hduls])
