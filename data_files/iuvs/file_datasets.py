from astropy.io import fits
from h5py import File


compression: str = 'gzip'
compression_opts: int = 4
# More info here: https://docs.h5py.org/en/stable/high/dataset.html#dataset-create

import binning
import detector
import instrument_geometry
import integration
import spacecraft_geometry
import spatial_bin_geometry
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


### Binning arrays ###
def add_spatial_bin_edges(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = binning.make_spatial_bin_edges(hduls)
    dataset = file[group_path].create_dataset('spatial_bin_edges', data=data, compression=compression,
                                               compression_opts=compression_opts)
    dataset.attrs['unit'] = units.pixel
    dataset.attrs['width'] = binning.make_bin_width(data)


def add_spectral_bin_edges(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = binning.make_spectral_bin_edges(hduls)
    dataset = file[group_path].create_dataset('spectral_bin_edges', data=data, compression=compression,
                                               compression_opts=compression_opts)
    dataset.attrs['unit'] = units.pixel
    dataset.attrs['width'] = binning.make_bin_width(data)


### Bin geometry arrays ###
def add_latitude(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_latitude(hduls, app_flip)
    dataset = file[group_path].create_dataset('latitude', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.latitude


def add_longitude(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_longitude(hduls, app_flip)
    dataset = file[group_path].create_dataset('longitude', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.longitude


def add_tangent_altitude(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_tangent_altitude(hduls, app_flip)
    dataset = file[group_path].create_dataset('tangent_altitude', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.altitude


def add_tangent_altitude_rate(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_tangent_altitude_rate(hduls, app_flip)
    dataset = file[group_path].create_dataset('tangent_altitude_rate', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.altitude_rate


def add_line_of_sight(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_line_of_sight(hduls, app_flip)
    dataset = file[group_path].create_dataset('line_of_sight', data=data, compression=compression,
                                              compression_opts=compression_opts)
    #dataset.attrs['unit'] = units.altitude_rate    # I dunno this value


def add_solar_zenith_angle(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_solar_zenith_angle(hduls, app_flip)
    dataset = file[group_path].create_dataset('solar_zenith_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_emission_angle(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_emission_angle(hduls, app_flip)
    dataset = file[group_path].create_dataset('emission_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_phase_angle(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_phase_angle(hduls, app_flip)
    dataset = file[group_path].create_dataset('phase_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_zenith_angle(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_zenith_angle(hduls, app_flip)
    dataset = file[group_path].create_dataset('zenith_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_local_time(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_local_time(hduls, app_flip)
    dataset = file[group_path].create_dataset('local_time', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.local_time


def add_right_ascension(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_right_ascension(hduls, app_flip)
    dataset = file[group_path].create_dataset('right_ascension', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_declination(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_declination(hduls, app_flip)
    dataset = file[group_path].create_dataset('declination', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_bin_vector(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = spatial_bin_geometry.make_spatial_bin_vector(hduls, app_flip)
    dataset = file[group_path].create_dataset('bin_vector', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.unit_vector


### Detector arrays ###
def add_raw(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = detector.make_detector_raw(hduls, app_flip)
    dataset = file[group_path].create_dataset('raw', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.data_number


def add_dark_subtracted(file: File, group_path: str, app_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    app_flip = file[f'{app_path}/app_flip'][:]
    data = detector.make_detector_raw(hduls, app_flip)
    dataset = file[group_path].create_dataset('dark_subtracted', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.data_number


def add_brightness(file: File, group_path: str, app_path: str, binning_path: str, integration_path: str, channel_integration_path: str, experiment: str) -> None:
    dark_subtracted = file[f'{group_path}/dark_subtracted'][:]
    spatial_bin_edges_ds = file[f'{binning_path}/spatial_bin_edges']
    spatial_bin_edges = spatial_bin_edges_ds[:]
    spatial_bin_width = spatial_bin_edges_ds.attrs['width']
    spectral_bin_edges_ds = file[f'{binning_path}/spectral_bin_edges']
    spectral_bin_edges = spectral_bin_edges_ds[:]
    spectral_bin_width = spectral_bin_edges_ds.attrs['width']

    good_integrations = file[f'{channel_integration_path}/{experiment}'][:]
    integration_time = file[f'{integration_path}/integration_time'][:][good_integrations]
    voltage = file[f'{channel_integration_path}/mcp_voltage'][:][good_integrations]
    voltage_gain = file[f'{channel_integration_path}/mcp_voltage_gain'][:][good_integrations]

    app_flip = file[f'{app_path}/app_flip'][:]
    data = detector.make_brightness(dark_subtracted, spatial_bin_edges, spatial_bin_width, spectral_bin_edges, spectral_bin_width,
                                    integration_time, voltage, voltage_gain, app_flip)

    dataset = file[group_path].create_dataset('brightness', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.brightness
