from pathlib import Path

import h5py

from _miscellaneous import Orbit


def make_hdf5_filename(orbit: int, save_location: Path) -> Path:
    orbit = Orbit(orbit)
    filename = f'{orbit.code}.hdf5'
    return save_location / orbit.block / filename


def open_latest_file(filepath: Path) -> h5py.File:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        f = h5py.File(filepath, mode='x')  # 'x' means to create the file but fail if it already exists
    except FileExistsError:
        f = h5py.File(filepath, mode='r+')  # 'r+' means read/write and file must exist
    return f


def make_empty_hdf5_groups(file: h5py.File) -> None:
    # This can be expanded to other segments if necessary
    make_empty_apoapse_groups(file)


def make_empty_apoapse_groups(file: h5py.File) -> None:
    # require_group will make it if it doesn't exist. Useful for adding groups in later version
    apoapse = file.require_group('apoapse')

    apoapse.require_group('apsis')
    apoapse.require_group('integration')
    apoapse.require_group('spacecraft_geometry')

    muv = apoapse.require_group('muv')

    muv.require_group('integration')
    dayside = muv.require_group('dayside')
    nightside = muv.require_group('nightside')

    dayside.require_group('binning')
    dayside.require_group('detector')
    dayside.require_group('pixel_geometry')
    dayside.require_group('retrievals')

    nightside.require_group('binning')
    nightside.require_group('detector')
    nightside.require_group('pixel_geometry')
    nightside.require_group('mlr')
