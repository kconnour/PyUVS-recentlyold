from astropy.io import fits
import numpy as np

import iuvs_fits


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_latitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_latitude(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_longitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_longitude(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_tangent_altitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_tangent_altitude(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_tangent_altitude_rate(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_tangent_altitude_rate(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_line_of_sight(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_line_of_sight(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_solar_zenith_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_solar_zenith_angle(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 2)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_emission_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_emission_angle(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 2)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_phase_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_phase_angle(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 2)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_zenith_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_zenith_angle(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 2)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_local_time(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_local_time(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 2)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_right_ascension(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_right_ascension(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_declination(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_declination(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 3)
    data = iuvs_fits.app_flip(data, flip)
    return np.concatenate(data)


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_vector(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [iuvs_fits.get_spatial_bin_vector(f) for f in hduls]
    data = iuvs_fits.add_leading_dimension_if_necessary(data, 4)
    data = iuvs_fits.app_flip(data, flip)
    data = np.concatenate(data)
    return np.moveaxis(data, 1, -1)
