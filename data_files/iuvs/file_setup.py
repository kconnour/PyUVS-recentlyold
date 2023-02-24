from pathlib import Path

from h5py import File

import pyuvs as pu


def make_hdf5_filename(orbit: int) -> str:
    return f'{pu.make_orbit_code(orbit)}.hdf5'


def make_hdf5_filepath(orbit: int, save_location: Path) -> Path:
    filename = make_hdf5_filename(orbit)
    return save_location / pu.orbit.make_orbit_block(orbit) / filename


def open_latest_file(orbit: int, data_file_save_location: Path) -> File:
    hdf5_filepath = make_hdf5_filepath(orbit, data_file_save_location)
    hdf5_filepath.parent.mkdir(parents=True, exist_ok=True)
    return File(hdf5_filepath, mode='a')  # 'a' means to create the file if it doesn't exist, read/write otherwise


def add_orbit_attribute_to_file(file: File, orbit: int) -> None:
    file.attrs['orbit'] = orbit
