from astropy.io import fits
import numpy as np

from pyuvs import apoapse_muv_failsafe_voltage, apoapse_muv_day_night_voltage_boundary
import iuvs_fits


@iuvs_fits.catch_empty_arrays
def make_timestamp(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_timestamp(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_ephemeris_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_ephemeris_time(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_utc(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_utc(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_mirror_data_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_mirror_data_number(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_mirror_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_mirror_angle(f) for f in hduls])


def make_integration_field_of_view(mirror_angle: np.ndarray) -> np.ndarray:
    return mirror_angle * 2


@iuvs_fits.catch_empty_arrays
def make_integration_lyman_alpha_centroid(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    # As of v13 IUVS data, this array is populated with junk data
    return np.concatenate([iuvs_fits.get_integration_lyman_alpha_centroid(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_detector_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_detector_temperature(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_case_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_case_temperature(f) for f in hduls])


@iuvs_fits.catch_empty_arrays
def make_integration_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = iuvs_fits.get_integrations_per_file(hduls)
    integration_time = [iuvs_fits.get_integration_time(f) for f in hduls]
    return np.repeat(integration_time, integrations_per_file)


@iuvs_fits.catch_empty_arrays
def make_data_file_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = iuvs_fits.get_integrations_per_file(hduls)
    file_index = np.arange(len(hduls))
    return np.repeat(file_index, integrations_per_file)


@iuvs_fits.catch_empty_arrays
def make_mcp_voltage(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = iuvs_fits.get_integrations_per_file(hduls)
    mcp_voltage = [iuvs_fits.get_mcp_voltage(f) for f in hduls]
    return np.repeat(mcp_voltage, integrations_per_file)


@iuvs_fits.catch_empty_arrays
def make_mcp_voltage_gain(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = iuvs_fits.get_integrations_per_file(hduls)
    mcp_voltage_gain = [iuvs_fits.get_mcp_voltage_gain(f) for f in hduls]
    return np.repeat(mcp_voltage_gain, integrations_per_file)


def make_apoapse_muv_failsafe_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    return np.isclose(mcp_voltage, apoapse_muv_failsafe_voltage)


def make_apoapse_muv_dayside_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    failsafe_integrations = make_apoapse_muv_failsafe_integrations(mcp_voltage)
    nightside_integrations = make_apoapse_muv_nightside_integrations(mcp_voltage)
    return ~(failsafe_integrations + nightside_integrations).astype('bool')


def make_apoapse_muv_nightside_integrations(mcp_voltage: np.ndarray) -> np.ndarray:
    return mcp_voltage > apoapse_muv_day_night_voltage_boundary


def convert_mcp_voltage_data_number_to_volts(data_number: np.ndarray) -> np.ndarray:
    # Note that I don't know where data number is in our data images but this creates the MCP volt structure
    return 0.244 * data_number - 1.83
