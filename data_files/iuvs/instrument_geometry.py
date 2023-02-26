from astropy.io import fits
from h5py import File
import numpy as np

from hdf5_options import compression, compression_opts
import units


def add_instrument_sun_angle_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_instrument_sun_angle_from_hduls(hduls)
    dataset = file[group_path].create_dataset('instrument_sun_angle', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.angle



def add_spacecraft_velocity_inertial_frame_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = add_spacecraft_velocity_inertial_frame_from_hduls(hduls)
    dataset = file[group_path].create_dataset('spacecraft_velocity_inertial_frame', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.velocity



def add_instrument_x_field_of_view_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = get_instrument_x_field_of_view_from_hduls(hduls)
    dataset = file[group_path].create_dataset('instrument_x_field_of_view', data=data,
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = units.field_of_view



def add_app_flip_to_file(file: File, group_path: str) -> None:
    vx = file[f'{group_path}/instrument_x_field_of_view']
    v = file[f'{group_path}/vx_instrument_inertial']
    data = compute_apoapse_app_flip(vx, v)
    dataset = file[group_path].create_dataset('app_flip', data=data,
                                              compression=compression, compression_opts=compression_opts)


def compute_apoapse_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0] > 0
        app_flip = np.array([np.mean(dot) >= 0.2])
    except IndexError:
        app_flip = np.array([])
    return app_flip
