from astropy.io import fits
from h5py import File

from app import compute_apoapse_app_flip
from iuvs_fits import get_instrument_x_field_of_view, get_instrument_sun_angle
from hdf5_options import compression, compression_opts
import units


def add_instrument_x_field_of_view_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_instrument_x_field_of_view(hduls)
    dataset = file[group_path].create_dataset('instrument_x_field_of_view', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.field_of_view


def add_instrument_sun_angle_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_instrument_sun_angle(hduls)
    dataset = file[group_path].create_dataset('instrument_sun_angle', data=data, compression=compression,
                                              compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle


def add_app_flip_to_file(file: File, group_path: str) -> None:
    vx = file[f'{group_path}/instrument_x_field_of_view']
    v = file[f'{group_path}/vx_instrument_inertial']
    data = compute_apoapse_app_flip(vx, v)
    dataset = file[group_path].create_dataset('app_flip', data=data, compression=compression,
                                              compression_opts=compression_opts)
