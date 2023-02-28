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
def get_detector_primary(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['primary'].data


def get_detector_raw(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['detector_raw'].data


def get_detector_dark_subtracted(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['detector_dark_subtracted'].data


def get_detector_random_data_number_uncertainty(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['random_dn_unc'].data


def get_detector_random_physical_uncertainty(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['random_phy_unc'].data


def get_detector_systematic_physical_uncertainty(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['systematic_phy_unc'].data


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
def get_subsolar_latitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['sub_solar_lat']


@catch_empty_arrays
def get_subsolar_longitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['sub_solar_lon']


@catch_empty_arrays
def get_subspacecraft_latitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['sub_spacecraft_lat']


@catch_empty_arrays
def get_subspacecraft_longitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['sub_spacecraft_lon']


@catch_empty_arrays
def get_subspacecraft_altitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['spacecraft_alt']


@catch_empty_arrays
def get_spacecraft_velocity_inertial_frame(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['v_spacecraft_rate_inertial']


### Instrument geometry ###
@catch_empty_arrays
def get_instrument_x_field_of_view(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['vx_instrument_inertial']


@catch_empty_arrays
def get_instrument_sun_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['spacecraftgeometry'].data['inst_sun_angle']


### Spatial bin geometry ###
def get_spatial_bin_latitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_lat']


def get_spatial_bin_longitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_lon']


def get_spatial_bin_tangent_altitude(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_mrh_alt']


def get_spatial_bin_tangent_altitude_rate(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_mrh_alt_rate']


def get_spatial_bin_line_of_sight(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_los']


def get_spatial_bin_solar_zenith_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_solar_zenith_angle']


def get_spatial_bin_emission_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_emission_angle']


def get_spatial_bin_phase_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_phase_angle']


def get_spatial_bin_zenith_angle(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_zenith_angle']


def get_spatial_bin_local_time(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_local_time']


def get_spatial_bin_right_ascension(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_ra']


def get_spatial_bin_declination(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_corner_dec']


def get_spatial_bin_vector(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    return hdul['pixelgeometry'].data['pixel_vec']


### Binning ###
def get_spatial_pixel_low(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    # The data is natively (1, n_spatial_bins)
    return hdul['binning'].data['spapixlo'][0]


def get_spatial_pixel_high(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    # The data is natively (1, n_spatial_bins)
    return hdul['binning'].data['spapixhi'][0]


def get_spectral_pixel_low(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    # The data is natively (1, n_spectral_bins)
    return hdul['binning'].data['spepixlo'][0]


def get_spectral_pixel_high(hdul: fits.hdu.hdulist.HDUList) -> np.ndarray:
    # The data is natively (1, n_spectral_bins)
    return hdul['binning'].data['spepixhi'][0]


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
