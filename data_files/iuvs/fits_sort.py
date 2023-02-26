from pathlib import Path

from astropy.io import fits
import numpy as np

import pyuvs as pu


def _get_segment_orbit_channel_fits_files(iuvs_fits_file_location: Path, segment: str, orbit: int, channel: str) -> list[Path]:
    orbit_block = pu.make_orbit_block(orbit)
    orbit_code = pu.make_orbit_code(orbit)
    return sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*{channel}*.gz'))


def get_apoapse_muv_fits_files(iuvs_fits_file_location: Path, orbit: int) -> list[fits.hdu.hdulist.HDUList]:
    data_files = _get_segment_orbit_channel_fits_files(iuvs_fits_file_location, 'apoapse', orbit, 'muv')
    return [fits.open(f) for f in data_files]
