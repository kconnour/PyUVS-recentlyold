from astropy.io import fits
import numpy as np

from iuvs_fits import catch_empty_arrays, get_integrations_per_file, get_integration_timestamp, get_integration_ephemeris_time, get_integration_utc, \
    get_integration_mirror_data_number, get_integration_mirror_angle, get_integration_lyman_alpha_centroid, \
    get_integration_detector_temperature, get_integration_case_temperature, get_integration_time


@catch_empty_arrays
def make_timestamp(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_timestamp(f) for f in hduls])


@catch_empty_arrays
def make_ephemeris_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_ephemeris_time(f) for f in hduls])


@catch_empty_arrays
def make_integration_utc(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_utc(f) for f in hduls])


@catch_empty_arrays
def make_integration_mirror_data_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_mirror_data_number(f) for f in hduls])


@catch_empty_arrays
def make_integration_mirror_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_mirror_angle(f) for f in hduls])


def make_integration_field_of_view(mirror_angle: np.ndarray) -> np.ndarray:
    return mirror_angle * 2


@catch_empty_arrays
def make_integration_lyman_alpha_centroid(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    # As of v13 IUVS data, this array is populated with junk data
    return np.concatenate([get_integration_lyman_alpha_centroid(f) for f in hduls])


@catch_empty_arrays
def make_integration_detector_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_detector_temperature(f) for f in hduls])


@catch_empty_arrays
def make_integration_case_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_case_temperature(f) for f in hduls])


@catch_empty_arrays
def make_integration_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    integration_time = [get_integration_time(f) for f in hduls]
    return np.repeat(integration_time, integrations_per_file)


@catch_empty_arrays
def make_data_file_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    file_index = np.arange(len(hduls))
    return np.repeat(file_index, integrations_per_file)
