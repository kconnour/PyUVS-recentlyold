import warnings

from astropy.io import fits
import numpy as np

import iuvs_fits


@iuvs_fits.catch_empty_arrays
def make_spatial_bin_edges(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    spatial_pixel_low = [iuvs_fits.get_spatial_pixel_low(f) for f in hduls]
    spatial_pixel_high = [iuvs_fits.get_spatial_pixel_high(f) for f in hduls]
    same_spatial_pixel_low = [f == spatial_pixel_low[0] for f in spatial_pixel_low]
    same_spatial_pixel_high = [f == spatial_pixel_high[0] for f in spatial_pixel_high]
    if not (np.all(same_spatial_pixel_low) and np.all(same_spatial_pixel_high)):
        raise IndexError('The file has different spatial binning schemes.')

    return np.append(spatial_pixel_low[0], spatial_pixel_high[0][-1] + 1)


@iuvs_fits.catch_empty_arrays
def make_spectral_bin_edges(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    spectral_pixel_low = [iuvs_fits.get_spectral_pixel_low(f) for f in hduls]
    spectral_pixel_high = [iuvs_fits.get_spectral_pixel_high(f) for f in hduls]
    same_spectral_pixel_low = [f == spectral_pixel_low[0] for f in spectral_pixel_low]
    same_spectral_pixel_high = [f == spectral_pixel_high[0] for f in spectral_pixel_high]
    if not (np.all(same_spectral_pixel_low) and np.all(same_spectral_pixel_high)):
        raise IndexError('The file has different spectral binning schemes.')

    return np.append(spectral_pixel_low[0], spectral_pixel_high[0][-1] + 1)


def make_bin_width(bin_edges: np.ndarray) -> int:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            width = int(np.median(np.diff(bin_edges)))
    except ValueError:
        width = 0
    return width
