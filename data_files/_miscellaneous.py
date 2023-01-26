import typing

from astropy.io import fits
import numpy as np


hdulist: typing.TypeAlias = fits.hdu.hdulist.HDUList


def add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
    return array if np.ndim(array) == expected_dims else array[None, :]


def get_integrations_per_file(hduls: list[hdulist]) -> list[int]:
    return [add_dimension_if_necessary(f['primary'].data, 3).shape[0] for f in hduls]
