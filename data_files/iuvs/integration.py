from astropy.io import fits
import numpy as np

from iuvs_fits import catch_empty_arrays, get_integration_timestamp, get_integration_ephemeris_time, \
    get_integration_mirror_data_number, get_integration_mirror_angle, get_integration_detector_temperature, get_integration_case_temperature


@catch_empty_arrays
def make_timestamp(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_timestamp(f) for f in hduls])


@catch_empty_arrays
def make_ephemeris_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([get_integration_ephemeris_time(f) for f in hduls])





'''@catch_empty_arrays
def get_integration_utc(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['utc'] for f in hduls])


@catch_empty_arrays
def get_integration_mirror_data_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls])


@catch_empty_arrays
def get_integration_mirror_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_deg'] for f in hduls])


@catch_empty_arrays
def get_integration_field_of_view(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['fov_deg'] for f in hduls])


@catch_empty_arrays
def get_integration_lyman_alpha_centroid(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    # As of v13 IUVS data, this array is populated with junk data
    return np.concatenate([f['integration'].data['lya_centroid'] for f in hduls])


@catch_empty_arrays
def get_integration_detector_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls])


@catch_empty_arrays
def get_integration_case_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls])


### Channel-independent arrays ###



def add_mirror_data_number_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_integration_mirror_data_number(hduls)
    dataset = file[group_path].create_dataset('mirror_data_number', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.data_number


def add_field_of_view_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_integration_field_of_view(hduls)
    dataset = file[group_path].create_dataset('field_of_view', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.field_of_view


def add_case_temperature_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_integration_case_temperature(hduls)
    dataset = file[group_path].create_dataset('case_temperature', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.temperature


def add_integration_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_integration_time(hduls)
    dataset = file[group_path].create_dataset('integration_time', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.integration_time


def add_data_file_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_data_file_number(hduls)
    dataset = file[group_path].create_dataset('data_file', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.integration_time


def add_apoapse_swath_number_to_file(file: File, group_path: str, orbit: int) -> None:
    field_of_view = file[f'{group_path}/field_of_view'][:]
    data = get_apoapse_swath_number(field_of_view, orbit)

    dataset = file[group_path].create_dataset('swath_number', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'The swath number of each integration.'


def add_apoapse_number_of_swaths_to_file(file: File, group_path: str, orbit: int) -> None:
    swath_number = file[f'{group_path}/swath_number'][:]
    data = get_apoapse_number_of_swaths(swath_number, orbit)

    dataset = file[group_path].create_dataset('n_swaths', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'The number of swaths intended for this observation sequence (not necessarily the number of swaths taken)'


def add_opportunity_classification_to_file(file: File, group_path: str) -> None:
    field_of_view = file[f'{group_path}/field_of_view'][:]
    swath_number = file[f'{group_path}/swath_number'][:]
    data = get_apoapse_opportunity_classification(field_of_view, swath_number)

    dataset = file[group_path].create_dataset('opportunity', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'True if an opportunistic observation; False otherwise.'


### Channel-dependent arrays ###
def add_detector_temperature_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_integration_detector_temperature(hduls)
    dataset = file[group_path].create_dataset('detector_temperature', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.temperature


def add_mcp_voltage_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_mcp_voltage(hduls)
    dataset = file[group_path].create_dataset('mcp_voltage', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.voltage


def add_mcp_voltage_gain_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_mcp_voltage_gain(hduls)
    dataset = file[group_path].create_dataset('mcp_voltage_gain', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.voltage


def add_apoapse_muv_failsafe_integrations_to_file(file: File, group_path: str) -> None:
    mcp_voltage = file[f'{group_path}/mcp_voltage'][:]
    data = apoapse_muv_failsafe_integrations(mcp_voltage)
    dataset = file[group_path].create_dataset('failsafe', data=data, compression=compression,
                                              compression_opts=compression_opts)


def add_apoapse_muv_dayside_integrations_to_file(file: File, group_path: str) -> None:
    mcp_voltage = file[f'{group_path}/mcp_voltage'][:]
    data = apoapse_muv_dayside_integrations(mcp_voltage)
    dataset = file[group_path].create_dataset('dayside', data=data, compression=compression,
                                              compression_opts=compression_opts)


def add_apoapse_muv_nightside_integrations_to_file(file: File, group_path: str) -> None:
    mcp_voltage = file[f'{group_path}/mcp_voltage'][:]
    data = apoapse_muv_nightside_integrations(mcp_voltage)
    dataset = file[group_path].create_dataset('nightside', data=data, compression=compression,
                                              compression_opts=compression_opts)'''
