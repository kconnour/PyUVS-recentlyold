from astropy.io import fits
from h5py import File


compression: str = 'gzip'
compression_opts: int = 4
# More info here: https://docs.h5py.org/en/stable/high/dataset.html#dataset-create

import instrument_geometry
import integration
import spacecraft_geometry
import swath
import units


### Channel-independent integration ####
def add_ephemeris_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_ephemeris_time(hduls)
    dataset = file[group_path].create_dataset('ephemeris_time', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.ephemeris_time


def add_mirror_data_number_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_integration_mirror_data_number(hduls)
    dataset = file[group_path].create_dataset('mirror_data_number', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.data_number


def add_mirror_angle_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_integration_mirror_angle(hduls)
    dataset = file[group_path].create_dataset('mirror_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_field_of_view_to_file(file: File, group_path: str) -> None:
    mirror_angle = file[f'{group_path}/mirror_angle'][:]
    data = integration.make_integration_field_of_view(mirror_angle)
    dataset = file[group_path].create_dataset('field_of_view', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.field_of_view


def add_case_temperature_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_integration_case_temperature(hduls)
    dataset = file[group_path].create_dataset('case_temperature', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.temperature


def add_integration_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_integration_time(hduls)
    dataset = file[group_path].create_dataset('integration_time', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.integration_time


def add_data_file_number_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_data_file_number(hduls)
    dataset = file[group_path].create_dataset('data_file', data=data, compression=compression,
                                              compression_opts=compression_opts)


def add_apoapse_swath_number_to_file(file: File, group_path: str, orbit: int) -> None:
    mirror_angle = file[f'{group_path}/mirror_angle'][:]
    data = swath.make_apoapse_swath_number(mirror_angle, orbit)

    dataset = file[group_path].create_dataset('swath_number', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'The swath number of each integration.'


def add_apoapse_number_of_swaths_to_file(file: File, group_path: str, orbit: int) -> None:
    swath_number = file[f'{group_path}/swath_number'][:]
    data = swath.make_apoapse_number_of_swaths(swath_number, orbit)

    dataset = file[group_path].create_dataset('n_swaths', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'The number of swaths intended for this observation sequence (not necessarily the ' \
                               'number of swaths taken)'


def add_apoapse_opportunity_classification_to_file(file: File, group_path: str, orbit: int) -> None:
    mirror_angle = file[f'{group_path}/mirror_angle'][:]
    swath_number = file[f'{group_path}/swath_number'][:]
    data = swath.make_apoapse_opportunity_classification(mirror_angle, swath_number, orbit)

    dataset = file[group_path].create_dataset('opportunity', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['comment'] = 'True if an opportunistic observation; False otherwise.'


### Spacecraft geometry ###
def add_subsolar_latitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_subsolar_latitude(hduls)
    dataset = file[group_path].create_dataset('subsolar_latitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.latitude


def add_subsolar_longitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_subsolar_longitude(hduls)
    dataset = file[group_path].create_dataset('subsolar_longitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_latitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_subspacecraft_latitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_latitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.latitude


def add_subspacecraft_longitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_subspacecraft_longitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_longitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_altitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_subspacecraft_altitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_altitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.altitude


def add_spacecraft_velocity_inertial_frame_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = spacecraft_geometry.make_spacecraft_velocity_inertial_frame(hduls)
    dataset = file[group_path].create_dataset('spacecraft_velocity_inertial_frame', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.velocity


### Instrument geometry ###
def add_instrument_x_field_of_view_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = instrument_geometry.make_instrument_x_field_of_view(hduls)
    dataset = file[group_path].create_dataset('instrument_x_field_of_view', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.field_of_view


def add_instrument_sun_angle_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = instrument_geometry.make_instrument_sun_angle(hduls)
    dataset = file[group_path].create_dataset('instrument_sun_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_app_flip_to_file(file: File, instrument_geometry_path: str, spacecraft_geometry_path: str) -> None:
    vx = file[f'{instrument_geometry_path}/instrument_x_field_of_view']
    v = file[f'{spacecraft_geometry_path}/spacecraft_velocity_inertial_frame']
    data = instrument_geometry.compute_app_flip(vx, v)
    dataset = file[instrument_geometry_path].create_dataset('app_flip', data=data)


### Channel-dependent arrays ###
def add_detector_temperature_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_integration_detector_temperature(hduls)
    dataset = file[group_path].create_dataset('detector_temperature', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.temperature


def add_mcp_voltage_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_mcp_voltage(hduls)
    dataset = file[group_path].create_dataset('mcp_voltage', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.voltage


def add_mcp_voltage_gain_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = integration.make_mcp_voltage_gain(hduls)
    dataset = file[group_path].create_dataset('mcp_voltage_gain', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.voltage


def add_apoapse_muv_failsafe_integrations_to_file(file: File, integration_path: str) -> None:
    mcp_voltage = file[f'{integration_path}/mcp_voltage'][:]
    data = integration.make_apoapse_muv_failsafe_integrations(mcp_voltage)
    dataset = file[integration_path].create_dataset('failsafe', data=data, compression=compression,
                                                    compression_opts=compression_opts)


def add_apoapse_muv_dayside_integrations_to_file(file: File, group_path: str) -> None:
    mcp_voltage = file[f'{group_path}/mcp_voltage'][:]
    data = integration.make_apoapse_muv_dayside_integrations(mcp_voltage)
    dataset = file[group_path].create_dataset('dayside', data=data, compression=compression,
                                              compression_opts=compression_opts)


def add_apoapse_muv_nightside_integrations_to_file(file: File, group_path: str) -> None:
    mcp_voltage = file[f'{group_path}/mcp_voltage'][:]
    data = integration.make_apoapse_muv_nightside_integrations(mcp_voltage)
    dataset = file[group_path].create_dataset('nightside', data=data, compression=compression,
                                              compression_opts=compression_opts)
