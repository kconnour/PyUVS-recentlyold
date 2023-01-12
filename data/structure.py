from pathlib import Path

import h5py

from iuvs_data_files import Orbit


class DataFile:
    def __init__(self, orbit: int, save_location: Path):
        self.orbit = Orbit(orbit)
        self.save_location = save_location

        self.filename = self._make_hdf5_filename()
        self.file = self._open_latest_file()

    def _make_hdf5_filename(self) -> Path:
        filename = f'{self.orbit.code}.hdf5'
        return self.save_location / self.orbit.block / filename

    def _open_latest_file(self) -> h5py.File:
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        try:
            f = h5py.File(self.filename, mode='x')  # 'x' means to create the file but fail if it already exists
        except FileExistsError:
            f = h5py.File(self.filename, mode='r+')  # 'r+' means read/write and file must exist
        return f

    def make_empty_hdf5_groups(self) -> None:
        # This can be expanded to other segments if necessary
        self._make_empty_apoapse_groups()

    def _make_empty_apoapse_groups(self) -> None:
        # require_group will make it if it doesn't exist. Useful for adding groups in later version
        apoapse = self.file.require_group('apoapse')

        apoapse.require_group('apsis')
        apoapse.require_group('engineering')
        apoapse.require_group('integration')

        muv = apoapse.require_group('muv')

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

    def close(self) -> None:
        self.file.close()
