import math
import typing

from astropy.io import fits
import numpy as np

from constants import day_night_voltage_boundary


hdulist: typing.TypeAlias = fits.hdu.hdulist.HDUList


def make_dataset_path(group_path: str, name: str) -> str:
    return f'{group_path}/{name}'


def add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
    return array if np.ndim(array) == expected_dims else array[None, :]


def get_integrations_per_file(hduls: list[hdulist]) -> list[int]:
    return [add_dimension_if_necessary(f['primary'].data, 3).shape[0] for f in hduls]


def determine_dayside_files(hduls: list[hdulist]) -> np.ndarray:
    return np.array([f['observation'].data['mcp_volt'][0] < day_night_voltage_boundary for f in hduls])


class Orbit:
    """A data structure containing info from an orbit number

    Parameters
    ----------
    orbit: int
        The MAVEN orbit number.

    Examples
    --------
    Create an orbit and get its properties.

    >>> orbit = Orbit(3453)
    >>> orbit.code
    'orbit03453'
    >>> orbit.block
    'orbit03400'

    """
    def __init__(self, orbit: int):
        self._orbit = orbit

        self._code = self._make_code()
        self._block = self._make_block()

    def _make_code(self) -> str:
        return 'orbit' + f'{self.orbit}'.zfill(5)

    def _make_block(self) -> str:
        block = math.floor(self.orbit / 100) * 100
        return 'orbit' + f'{block}'.zfill(5)

    @property
    def orbit(self) -> int:
        """Get the input orbit.

        """
        return self._orbit

    @property
    def code(self) -> str:
        """Get the IUVS "orbit code" for the input orbit.

        """
        return self._code

    @property
    def block(self) -> str:
        """Get the IUVS orbit block for the input orbit.

        """
        return self._block
