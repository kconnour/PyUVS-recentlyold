from astropy.io import fits
from h5py import File
import numpy as np

from hdf5_options import compression, compression_opts
import units


def get_ephemeris_time_from_hduls(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])





def add_development_dataset_to_file(file: File, group_path: str, dataset_name: str, unit: str, latest_version: int, get_data: callable, *args) -> None:
    dataset_path = f'{group_path}/{dataset_name}'
    if dataset_path not in file:
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(args),
                                                  compression=compression, compression_opts=compression_opts)
        dataset.attrs['unit'] = unit
        dataset.attrs['version'] = latest_version
    else:
        dataset = file[dataset_path]
        if dataset.attrs['version'] != latest_version:
            dataset[:] = get_data(args)
            dataset.attrs['version'] = latest_version


def add_production_dataset_to_file(file: File, group_path: str, dataset_name: str, unit: str, get_data: callable, *args) -> None:
    dataset = file[group_path].create_dataset(dataset_name, data=get_data(args),
                                              compression=compression, compression_opts=compression_opts)
    dataset.attrs['unit'] = unit


def get_latest_ephemeris_time_pipeline():
    return 'ephemeris_time', units.ephemeris_time, 1, get_ephemeris_time_from_hduls


def add_development_ephemeris_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    pipeline = get_latest_ephemeris_time_pipeline()
    add_development_dataset_to_file(file, group_path, pipeline[0], pipeline[1], pipeline[2], pipeline[3], hduls)


def add_production_ephemeris_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    pipeline = get_latest_ephemeris_time_pipeline()
    add_production_dataset_to_file(file, group_path, pipeline[0], pipeline[1], pipeline[3], hduls)


'''def add_ephemeris_time_to_file(file: File, group_path: str, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    dataset_name = 'ephemeris_time'
    latest_version = 1
    func = get_ephemeris_time_from_hduls
    add_dataset_to_file(file, group_path, dataset_name, units.ephemeris_time, latest_version, func, hduls)'''



#def get_field_of_view_from_hduls(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
#    return np.concatenate([f['integration'].data['fov_deg'] for f in hduls]) if hduls else np.array([])
