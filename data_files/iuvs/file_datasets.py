from astropy.io import fits
from h5py import File


compression: str = 'gzip'
compression_opts: int = 4
# More info here: https://docs.h5py.org/en/stable/high/dataset.html#dataset-create

from integration import make_ephemeris_time
import units


def add_ephemeris_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_ephemeris_time(hduls)
    dataset = file[group_path].create_dataset('ephemeris_time', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.ephemeris_time
