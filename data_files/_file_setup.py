from pathlib import Path

import h5py

import pyuvs as pu


def create_file(orbit: int, version: int, data_file_save_location: Path) -> h5py.File:
    hdf5_filepath = make_hdf5_filepath(orbit, version, data_file_save_location)
    return open_latest_file(hdf5_filepath)


def make_hdf5_filename(orbit: int, version: int) -> str:
    version_code = f'{version}'.zfill(2)
    return f'{pu.orbit.make_orbit_code(orbit)}_v{version_code}.hdf5'


def make_hdf5_filepath(orbit: int, version: int, save_location: Path) -> Path:
    filename = make_hdf5_filename(orbit, version)
    return save_location / pu.orbit.make_orbit_block(orbit) / filename


def open_latest_file(hdf5_filepath: Path) -> h5py.File:
    hdf5_filepath.parent.mkdir(parents=True, exist_ok=True)
    return h5py.File(hdf5_filepath, mode='x')  # 'x' means to create the file but fail if it already exists


def add_basic_attributes_to_file(file: h5py.File, orbit: int, version: int) -> None:
    file.attrs['orbit'] = orbit
    file.attrs['version'] = version
