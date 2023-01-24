import h5py
import mer
import numpy as np
import spiceypy

from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions
from _miscellaneous import make_dataset_path, haversine
import _spice as spice


def add_apsis_ephemeris_time(file: h5py.File, group_path: str, ephemeris_times: np.ndarray) -> None:
    def get_data() -> np.ndarray:
        orbit = file.attrs['orbit']
        return np.array([ephemeris_times[orbit-1]])

    dataset_name = 'ephemeris_time'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Seconds since J2000'
        dataset.attrs['comment'] = 'Computed with SPICE with 1 minute step sizes.'


def add_mars_year(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        utc = spiceypy.et2datetime(et)
        return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_whole_mars_year()])

    dataset_name = 'mars_year'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Years'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to Mars year via mer.'


def add_solar_longitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_solar_longitude(et)])

    dataset_name = 'solar_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to solar longitude via SPICE.'


def add_sol(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        utc = spiceypy.et2datetime(et)
        return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_sol()])

    dataset_name = 'sol'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Day of the year'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to sol via mer.'


def add_subsolar_latitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_subsolar_point(et)[0]])

    dataset_name = 'subsolar_latitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees [N]'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subsolar point via SPICE.'


def add_subsolar_longitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_subsolar_point(et)[1]])

    dataset_name = 'subsolar_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees [E]'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subsolar point via SPICE.'


def add_subspacecraft_latitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_subspacecraft_point(et)[0]])

    dataset_name = 'subspacecraft_latitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees [N]'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_longitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_subspacecraft_point(et)[1]])

    dataset_name = 'subspacecraft_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees [E]'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_altitude(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_subspacecraft_altitude(et)])

    dataset_name = 'subspacecraft_altitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'km'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_subspacecraft_local_time(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        longitude = file.file[f'{group_path}/sub_spacecraft_longitude'][:][0]
        return np.array([spice.compute_subspacecraft_local_time(et, np.radians(longitude))])

    dataset_name = 'subspacecraft_local_time'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Hours'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the subspacecraft point via SPICE.'


def add_mars_sun_distance(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.compute_mars_sun_distance(et)])

    dataset_name = 'mars_sun_distance'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'km'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE ' \
              'then converting the ephemeris time to the Mars-sun distance via SPICE.'


def add_subsolar_subspacecraft_angle(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        sub_solar_latitude = file[f'{group_path}/subsolar_latitude'][:][0]
        sub_solar_longitude = file[f'{group_path}/subsolar_longitude'][:][0]
        sub_spacecraft_latitude = file[f'{group_path}/subspacecraft_latitude'][:][0]
        sub_spacecraft_longitude = file[f'{group_path}/subspacecraft_longitude'][:][0]
        return np.array([haversine(sub_solar_latitude, sub_solar_longitude, sub_spacecraft_latitude, sub_spacecraft_longitude)])

    dataset_name = 'subsolar_subspacecraft_angle'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]

    if not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = 'Degrees'
        dataset.attrs['comment'] = 'Created by computing the apsis ephemeris time with SPICE, ' \
              'computing the subsolar and subspacecraft points at that ephemeris time,' \
              'and finally computing the haversine of those points.'
