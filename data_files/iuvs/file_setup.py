from pathlib import Path

from h5py import File

import pyuvs as pu


def make_hdf5_filename(orbit: int, version: int) -> str:
    version_code = f'{version}'.zfill(2)
    return f'{pu.make_orbit_code(orbit)}_v{version_code}.hdf5'


def make_hdf5_filepath(orbit: int, version: int, save_location: Path) -> Path:
    filename = make_hdf5_filename(orbit, version)
    return save_location / pu.orbit.make_orbit_block(orbit) / filename


def open_latest_file(orbit: int, version: int, data_file_save_location: Path) -> File:
    hdf5_filepath = make_hdf5_filepath(orbit, version, data_file_save_location)
    hdf5_filepath.parent.mkdir(parents=True, exist_ok=True)
    return File(hdf5_filepath, mode='a')  # 'x' means to create the file but fail if it exists


def add_orbit_attribute_to_file(file: File, orbit: int) -> None:
    file.attrs['orbit'] = orbit


def add_version_attribute_to_file(file: File, version: int) -> None:
    file.attrs['version'] = version
