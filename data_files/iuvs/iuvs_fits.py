from astropy.io import fits
import numpy as np


def catch_empty_arrays(func: callable):
    def wrapper(hduls: list[fits.hdu.hdulist.HDUList], *args):
        return func(hduls, *args) if hduls else np.array([])
    return wrapper


def add_leading_dimension_if_necessary(data: list[np.ndarray], expected_dims: int) -> list[np.ndarray]:
    return [f if np.ndim(f)==expected_dims else f[None, :] for f in data if f.size>0]


def app_flip(data: list[np.ndarray], flip: bool) -> list[np.ndarray]:
    return [np.fliplr(np.flipud(f)) if flip else f for f in data]


def get_integrations_per_file(hduls: list[fits.hdu.hdulist.HDUList]) -> list[int]:
    et = [f['integration'].data['et'] for f in hduls]
    return [f.shape[0] for f in et]


### Detector ###
@catch_empty_arrays
def get_detector_primary(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['primary'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_detector_raw(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['detector_raw'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_detector_dark_subtracted(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['detector_dark_subtracted'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_detector_random_data_number_uncertainty(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['random_dn_unc'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_detector_random_physical_uncertainty(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['random_phy_unc'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_detector_systematic_physical_uncertainty(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['systematic_phy_unc'].data for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


### Integration ###
def get_integration_timestamp(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['timestamp']


def get_integration_ephemeris_time(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['et']


def get_integration_utc(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['utc']


def get_integration_mirror_data_number(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['mirror_dn']


def get_integration_mirror_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['mirror_deg']


def get_integration_field_of_view(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['fov_deg']


def get_integration_lyman_alpha_centroid(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    # As of v13 IUVS data, this array is populated with junk data
    return hdul['integration'].data['lya_centroid']


def get_integration_detector_temperature(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['det_temp_c']


def get_integration_case_temperature(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['integration'].data['case_temp_c']


### Spacecraft geometry ###
@catch_empty_arrays
def get_subsolar_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls])


@catch_empty_arrays
def get_subsolar_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls])


@catch_empty_arrays
def get_subspacecraft_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls])


@catch_empty_arrays
def get_subspacecraft_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls])


@catch_empty_arrays
def get_subspacecraft_altitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls])


@catch_empty_arrays
def get_spacecraft_velocity_inertial_frame(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls])


### Instrument geometry ###
@catch_empty_arrays
def get_instrument_x_field_of_view(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls])


@catch_empty_arrays
def get_instrument_sun_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls])


### Spatial bin geometry ###
@catch_empty_arrays
def get_spatial_bin_latitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_lat'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_longitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_lon'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_tangent_altitude(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_mrh_alt'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_tangent_altitude_rate(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_mrh_alt_rate'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_line_of_sight(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_los'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_solar_zenith_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_solar_zenith_angle'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 2)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_emission_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_emission_angle'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 2)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_phase_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_phase_angle'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 2)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_zenith_angle(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_zenith_angle'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 2)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_local_time(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_local_time'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 2)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_right_ascension(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_ra'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_declination(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_corner_dec'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 3)
    data = app_flip(data, flip)
    return np.concatenate(data)


@catch_empty_arrays
def get_spatial_bin_vector(hduls: list[fits.hdu.hdulist.HDUList], flip: bool) -> np.ndarray:
    data = [f['pixelgeometry'].data['pixel_vec'] for f in hduls]
    data = add_leading_dimension_if_necessary(data, 4)
    data = app_flip(data, flip)
    data = np.concatenate(data)
    return np.moveaxis(data, 1, -1)


### Observation ###
def get_channel(hdul: fits.hdu.hdulist.HDUList) -> float:
    return hdul['observation'].data['channel'][0]


def get_integration_time(hdul: fits.hdu.hdulist.HDUList) -> float:
    return hdul['observation'].data['int_time'][0]


def get_mcp_voltage(hdul: fits.hdu.hdulist.HDUList) -> float:
    return hdul['observation'].data['mcp_volt'][0]


def get_mcp_voltage_gain(hdul: fits.hdu.hdulist.HDUList) -> float:
    return hdul['observation'].data['mcp_gain'][0]


def get_observation_id(hdul: fits.hdu.hdulist.HDUList) -> int:
    # This is found here and nowhere else to my knowledge
    return hdul['primary'].header['obs_id']


### Oddball ###
@catch_empty_arrays
def get_data_file_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    file_number = np.arange(len(integrations_per_file))
    return np.repeat(file_number, integrations_per_file)
