import warnings

import numpy as np

from pyuvs.anc import load_muv_flatfield_v1, load_voltage_correction_voltage, \
    load_voltage_correction_coefficients, load_muv_sensitivity_curve_observational
from pyuvs.constants import latest_hdul_file_version, pixel_angular_size
from pyuvs.file_classification import add_dimension_if_necessary
from pyuvs.typing import hdulist


def get_raw_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['detector_raw'].data, 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def get_dark_subtracted_from_hduls(hduls: hdulist, app_flip: bool) -> np.ndarray:
    if hduls:
        data = np.concatenate([add_dimension_if_necessary(f['detector_dark_subtracted'].data, 3) for f in hduls])
        data = np.fliplr(data) if app_flip else data
    else:
        data = np.array([])
    return data


def _make_muv_flatfield(spatial_bin_edges: np.ndarray, spectral_bin_edges: np.ndarray) -> np.ndarray:
    original_flatfield = load_muv_flatfield_v1()

    spatial_bins = spatial_bin_edges.shape[0] - 1
    spectral_bins = spectral_bin_edges.shape[0] - 1

    new_flatfield = np.zeros((spatial_bins, spectral_bins))
    for spatial_bin in range(spatial_bins):
        for spectral_bin in range(spectral_bins):
            new_flatfield[spatial_bin, spectral_bin] = np.mean(
                original_flatfield[spatial_bin_edges[spatial_bin]: spatial_bin_edges[spatial_bin + 1],
                spectral_bin_edges[spectral_bin]: spectral_bin_edges[spectral_bin + 1]])
    return new_flatfield


def _make_gain_correction(dark_subtracted, spatial_bin_width, spectral_bin_width, integration_time, mcp_volt, mcp_gain):
    """

    Parameters
    ----------
    dds: np.ndarray
        The detector dark subtacted
    spa_size: int
        The number of detector pixels in a spatial bin
    spe_size: int
        The number of detector pixels in a spectral bin
    integration_time
    mcp_volt
    mcp_gain

    Returns
    -------

    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        volt_array = load_voltage_correction_voltage()
        ab = load_voltage_correction_coefficients()
        ref_mcp_gain = 50.909455

        normalized_img = dark_subtracted.T / integration_time / spatial_bin_width / spectral_bin_width

        a = np.interp(mcp_volt, volt_array, ab[:, 0])
        b = np.interp(mcp_volt, volt_array, ab[:, 1])

        norm_img = np.exp(a + b * np.log(normalized_img))
        return (norm_img / normalized_img * mcp_gain / ref_mcp_gain).T


def make_brightness(dark_subtracted: np.ndarray, spatial_bin_edges: np.ndarray, spatial_bin_width: int,
                    spectral_bin_edges: np.ndarray, spectral_bin_width: int, integration_time: np.ndarray,
                    mcp_voltage: np.ndarray, mcp_voltage_gain: np.ndarray, app_flip: bool) -> np.ndarray:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if dark_subtracted.size > 0:
            # Get the flatfield
            flatfield = _make_muv_flatfield(spatial_bin_edges, spectral_bin_edges)

            # The sensitivity curve is currently 512 elements. Make it (1024,) for simplicity
            sensitivity_curve = load_muv_sensitivity_curve_observational()[:, 1]
            sensitivity_curve = np.repeat(sensitivity_curve, 2)

            # Get the sensitivity in each spectral bin
            # For array shape reasons, I spread this out over several lines
            rebinned_sensitivity_curve = np.array([np.mean(sensitivity_curve[spectral_bin_edges[i]:spectral_bin_edges[i + 1]]) for i in range(spectral_bin_edges.shape[0] - 1)])
            partial_corrected_brightness = dark_subtracted / rebinned_sensitivity_curve * 4 * np.pi * 10 ** -9 / pixel_angular_size / spatial_bin_width
            partial_corrected_brightness = (partial_corrected_brightness.T / mcp_voltage_gain / integration_time).T

            # Finally, do the voltage gain and flatfield corrections
            voltage_correction = _make_gain_correction(dark_subtracted, spatial_bin_width, spectral_bin_width, integration_time, mcp_voltage, mcp_voltage_gain)
            data = partial_corrected_brightness / flatfield * voltage_correction

            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data


raw_hdul_comment: str = f'This data is taken from the pixelgeometry/detector_raw structure of the version {latest_hdul_file_version} IUVS data.'
dark_subtracted_hdul_comment: str = f'This data is taken from the pixelgeometry/detector_dark_subtracted structure of the version {latest_hdul_file_version} IUVS data.'
brightness_comment: str = 'This data starts from the dark_subtracted and applies a flatfield and voltage gain correction.'
