import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/spacecraft_geometry'


def add_spacecraft_geometry_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_subsolar_latitude(file, hduls)
    add_subsolar_longitude(file, hduls)
    add_subspacecraft_latitude(file, hduls)
    add_subspacecraft_longitude(file, hduls)
    add_subspacecraft_altitude(file, hduls)
    add_instrument_sun_angle(file, hduls)
    add_spacecraft_velocity_inertial_frame(file, hduls)
    add_instrument_x_field_of_view(file, hduls)
    add_app_flip(file)


def add_subsolar_latitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subsolar_latitude_from_hduls(hduls)

    dataset = file[path].create_dataset('subsolar_latitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.latitude
    dataset.attrs['comment'] = pu.spacecraft_geometry.subsolar_latitude_hdul_comment


def add_subsolar_longitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subsolar_longitude_from_hduls(hduls)

    dataset = file[path].create_dataset('subsolar_longitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.longitude
    dataset.attrs['comment'] = pu.spacecraft_geometry.subsolar_longitude_hdul_comment


def add_subspacecraft_latitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_latitude_from_hduls(hduls)

    dataset = file[path].create_dataset('subspacecraft_latitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.latitude
    dataset.attrs['comment'] = pu.spacecraft_geometry.subspacecraft_latitude_hdul_comment


def add_subspacecraft_longitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_longitude_from_hduls(hduls)

    dataset = file[path].create_dataset('subspacecraft_longitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.longitude
    dataset.attrs['comment'] = pu.spacecraft_geometry.subspacecraft_longitude_hdul_comment


def add_subspacecraft_altitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_subspacecraft_altitude_from_hduls(hduls)

    dataset = file[path].create_dataset('subspacecraft_altitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.altitude
    dataset.attrs['comment'] = pu.spacecraft_geometry.subspacecraft_altitude_hdul_comment


def add_instrument_sun_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_instrument_sun_angle_from_hduls(hduls)

    dataset = file[path].create_dataset('instrument_sun_angle', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.instrument_sun_angle
    dataset.attrs['comment'] = pu.spacecraft_geometry.instrument_sun_angle_hdul_comment


def add_spacecraft_velocity_inertial_frame(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.add_spacecraft_velocity_inertial_frame_from_hduls(hduls)

    dataset = file[path].create_dataset('spacecraft_velocity_inertial_frame', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.velocity
    dataset.attrs['comment'] = pu.spacecraft_geometry.spacecraft_velocity_inertial_frame_comment


def add_instrument_x_field_of_view(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return pu.spacecraft_geometry.get_instrument_x_field_of_view_from_hduls(hduls)

    dataset = file[path].create_dataset('instrument_x_field_of_view', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.unit_vector
    dataset.attrs['comment'] = pu.spacecraft_geometry.instrument_x_field_of_view_hdul_comment


def add_app_flip(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        vx = file[f'{path}/instrument_x_field_of_view'][:]
        sc_rate = file[f'{path}/spacecraft_velocity_inertial_frame'][:]
        return pu.spacecraft_geometry.compute_app_flip(vx, sc_rate)

    segment_path = 'apoapse'
    dataset = file[segment_path].create_dataset('app_flip', data=get_data())
    dataset.attrs['comment'] = pu.spacecraft_geometry.app_flip_comment
