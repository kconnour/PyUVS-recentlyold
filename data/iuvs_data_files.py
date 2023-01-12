import math
from pathlib import Path

from astropy.io import fits
import numpy as np

from constants import day_night_voltage_boundary


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

class DataFinder:
    def __init__(self, data_directory: Path, orbit: int, segment: str, channel: str):
        self.data_directory = data_directory
        self.orbit = Orbit(orbit)
        self.segment = segment
        self.channel = channel

        self._original_hduls = self._get_original_hduls()
        self.hduls = self._original_hduls

    def _get_original_hduls(self):
        files = self._get_all_orbit_segment_channel_files()
        return [fits.open(f) for f in files]

    def _get_all_orbit_segment_channel_files(self) -> list[Path]:
        return sorted((self.data_directory / self.orbit.block).glob(f'*{self.segment}*{self.orbit.code}*{self.channel}*.gz'))

    def keep_daynight_hduls(self, dayside: bool):
        daynight_files = self._determine_dayside_files(self.hduls) == dayside
        self.hduls = [self.hduls[c] for c, f in enumerate(daynight_files) if f]

    def reset_hduls(self):
        self.hduls = self._original_hduls

    @staticmethod
    def _determine_dayside_files(hduls) -> np.ndarray:
        return np.array([f['observation'].data['mcp_volt'][0] < day_night_voltage_boundary for f in hduls])

    @staticmethod
    def _add_dimension_if_necessary(array: np.ndarray, expected_dims: int) -> np.ndarray:
        return array if np.ndim(array) == expected_dims else array[None, :]

    '''def get_ephemeris_time(self):
        return np.concatenate([f['integration'].data['et'] for f in self.hduls])

    def get_field_of_view(self):
        return self._get_sub_array('integration', 'fov_deg')

    def get_detector_temperature(self):
        return self._get_sub_array('integration', 'det_temp_c')

    def get_case_temperature(self):
        return self._get_sub_array('integration', 'case_temp_c')'''


if __name__ == '__main__':
    df = DataFinder(Path('/media/kyle/iuvs/production'), 4000, 'apoapse', 'muv')
    df.keep_daynight_hduls(True)
    print(df.get_latitude().shape)
    df.reset_hduls()
    df.keep_daynight_hduls(False)
    print(df.get_latitude().shape)