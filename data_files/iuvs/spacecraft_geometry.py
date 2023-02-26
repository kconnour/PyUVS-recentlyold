from astropy.io import fits
from h5py import File

from iuvs_fits import get_subsolar_latitude, get_subsolar_longitude, get_subspacecraft_latitude, \
    get_subspacecraft_longitude, get_subspacecraft_altitude
from hdf5_options import compression, compression_opts
import units


def add_subsolar_latitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_subsolar_latitude(hduls)
    dataset = file[group_path].create_dataset('subsolar_latitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.latitude


def add_subsolar_longitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_subsolar_longitude(hduls)
    dataset = file[group_path].create_dataset('subsolar_longitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_latitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_subspacecraft_latitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_latitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.latitude


def add_subspacecraft_longitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_subspacecraft_longitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_longitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_altitude_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_subspacecraft_altitude(hduls)
    dataset = file[group_path].create_dataset('subspacecraft_altitude', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.altitude
