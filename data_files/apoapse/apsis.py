import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/apsis'


def add_apsis_data_to_file(file: h5py.File, approximate_ephemeris_times: np.ndarray) -> None:
    add_apsis_ephemeris_time(file, approximate_ephemeris_times)
    add_mars_year(file)
    add_solar_longitude(file)
    add_sol(file)
    add_subsolar_latitude(file)
    add_subsolar_longitude(file)
    add_subspacecraft_latitude(file)
    add_subspacecraft_longitude(file)
    add_subspacecraft_altitude(file)
    add_subspacecraft_local_time(file)
    add_mars_sun_distance(file)
    add_subsolar_subspacecraft_angle(file)


def get_ephemeris_time_from_file(file: h5py.File) -> float:
    return file[f'{path}/ephemeris_time'][:][0]


def add_apsis_ephemeris_time(file: h5py.File, ephemeris_times: np.ndarray) -> None:
    def get_data() -> np.ndarray:
        orbit = file.attrs['orbit']
        return pu.apsis.get_ephemeris_time(ephemeris_times, orbit)

    dataset = file[path].create_dataset('ephemeris_time', data=get_data())
    dataset.attrs['unit'] = pu.units.ephemeris_time
    dataset.attrs['comment'] = 'Computed with SPICE with 1 minute step sizes.'


def add_mars_year(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_mars_year(et)

    dataset = file[path].create_dataset('mars_year', data=get_data())
    dataset.attrs['unit'] = pu.units.mars_year
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to Mars year via mer.'


def add_solar_longitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_solar_longitude(et)

    dataset = file[path].create_dataset('solar_longitude', data=get_data())
    dataset.attrs['unit'] = pu.units.solar_longitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to solar longitude via SPICE.'


def add_sol(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_sol(et)

    dataset = file[path].create_dataset('sol', data=get_data())
    dataset.attrs['unit'] = pu.units.sol
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to sol via mer.'


def add_subsolar_latitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_subsolar_latitude(et)

    dataset = file[path].create_dataset('subsolar_latitude', data=get_data())
    dataset.attrs['unit'] = pu.units.latitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subsolar point via SPICE.'


def add_subsolar_longitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_subsolar_longitude(et)

    dataset = file[path].create_dataset('subsolar_longitude', data=get_data())
    dataset.attrs['unit'] = pu.units.longitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
                               'then converting the ephemeris time to the subsolar point via SPICE.'


def add_subspacecraft_latitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_subspacecraft_latitude(et)

    dataset = file[path].create_dataset('subspacecraft_latitude', data=get_data())
    dataset.attrs['unit'] = pu.units.latitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_longitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_subspacecraft_latitude(et)

    dataset = file[path].create_dataset('subspacecraft_longitude', data=get_data())
    dataset.attrs['unit'] = pu.units.longitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
                               'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_altitude(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        return pu.apsis.compute_subspacecraft_altitude(et)

    dataset = file[path].create_dataset('subspacecraft_altitude', data=get_data())
    dataset.attrs['unit'] = pu.units.altitude
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_local_time(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = get_ephemeris_time_from_file(file)
        longitude = file.file[f'{path}/subspacecraft_longitude'][:][0]
        return pu.apsis.compute_subspacecraft_local_time(et, longitude)

    dataset = file[path].create_dataset('subspacecraft_local_time', data=get_data())
    dataset.attrs['unit'] = pu.units.local_time
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_mars_sun_distance(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{path}/ephemeris_time'][:][0]
        return pu.apsis.compute_mars_sun_distance(et)

    dataset = file[path].create_dataset('mars_sun_distance', data=get_data())
    dataset.attrs['unit'] = pu.units.local_time
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the Mars-sun distance via SPICE.'


def add_subsolar_subspacecraft_angle(file: h5py.File) -> None:
    def get_data() -> np.ndarray:
        sub_solar_latitude = file[f'{path}/subsolar_latitude'][:][0]
        sub_solar_longitude = file[f'{path}/subsolar_longitude'][:][0]
        sub_spacecraft_latitude = file[f'{path}/subspacecraft_latitude'][:][0]
        sub_spacecraft_longitude = file[f'{path}/subspacecraft_longitude'][:][0]
        return np.array([pu.angle.haversine(sub_solar_latitude, sub_solar_longitude, sub_spacecraft_latitude, sub_spacecraft_longitude)])

    dataset = file[path].create_dataset('subsolar_subspacecraft_angle', data=get_data())
    dataset.attrs['unit'] = pu.units.angle
    dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE, ' \
              'computing the subsolar and subspacecraft points at that ephemeris time,' \
              'and finally computing the haversine of those points.'
