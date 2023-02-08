import h5py
import numpy as np

import pyuvs as pu

group_path = 'apoapse/muv/dayside/bin_geometry'


def add_bin_geometry_data_to_file(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    add_latitude(file, hduls)
    add_longitude(file, hduls)
    add_tangent_altitude(file, hduls)
    add_tangent_altitude_rate(file, hduls)
    add_line_of_sight(file, hduls)
    add_solar_zenith_angle(file, hduls)
    add_emission_angle(file, hduls)
    add_phase_angle(file, hduls)
    add_zenith_angle(file, hduls)
    add_local_time(file, hduls)
    add_right_ascension(file, hduls)
    add_declination(file, hduls)
    add_bin_vector(file, hduls)


def get_app_flip(file: h5py.File) -> bool:
    return file[f'apoapse/app_flip'][:]


def add_latitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_latitude_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('latitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.latitude
    dataset.attrs['comment'] = pu.bin_geometry.latitude_hdul_comment


def add_longitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_longitude_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('longitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.longitude
    dataset.attrs['comment'] = pu.bin_geometry.longitude_hdul_comment


def add_tangent_altitude(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_tangent_altitude_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('tangent_altitude', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.altitude
    dataset.attrs['comment'] = pu.bin_geometry.tangent_altitude_hdul_comment


def add_tangent_altitude_rate(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_tangent_altitude_rate_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('tangent_altitude_rate', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.altitude
    dataset.attrs['comment'] = pu.bin_geometry.tangent_altitude_rate_hdul_comment


def add_line_of_sight(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_line_of_sight_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('line_of_sight', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['comment'] = pu.bin_geometry.line_of_sight_hdul_comment


def add_solar_zenith_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_solar_zenith_angle_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('solar_zenith_angle', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.solar_zenith_angle_hdul_comment


def add_emission_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_emission_angle_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('emission_angle', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.emission_angle_hdul_comment


def add_phase_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_phase_angle_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('phase_angle', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.phase_angle_hdul_comment


def add_zenith_angle(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_zenith_angle_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('zenith_angle', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.zenith_angle_hdul_comment


def add_local_time(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_local_time_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('local_time', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.local_time
    dataset.attrs['comment'] = pu.bin_geometry.local_time_hdul_comment


def add_right_ascension(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_right_ascension_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('right_ascension', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.right_ascension_hdul_comment


def add_declination(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_declination_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('declination', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = pu.bin_geometry.declination_hdul_comment


def add_bin_vector(file: h5py.File, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        app = get_app_flip(file)
        return pu.bin_geometry.get_bin_vector_from_hduls(hduls, app)

    dataset = file[group_path].create_dataset('bin_vector', data=get_data(), compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.unit_vector
    dataset.attrs['comment'] = pu.bin_geometry.bin_vector_hdul_comment
