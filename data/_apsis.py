import mer
import numpy as np
import spiceypy

from _structure import DataFile
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, haversine
import _spice as spice


def add_orbit_ephemeris_time(data_file: DataFile, group_path: str, ephemeris_times: np.ndarray) -> None:
    def get_data() -> np.ndarray:
        orbit = data_file.file.attrs['orbit']
        return np.array([ephemeris_times[orbit-1]])

    dataset_name = 'ephemeris_time'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Seconds since J2000'
    comment = 'Computed with SPICE with 1 minute temporal resolution.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mars_year(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        utc = spiceypy.et2datetime(et)
        return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_whole_mars_year()])

    dataset_name = 'mars_year'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = ''
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_solar_longitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.generic.compute_solar_longitude(et)])

    dataset_name = 'solar_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sol(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        utc = spiceypy.et2datetime(et)
        return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_sol()])

    dataset_name = 'sol'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Day of the year'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_solar_latitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.generic.compute_subsolar_point(et)[0]])

    dataset_name = 'sub_solar_latitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [N]'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_solar_longitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        print(spice.generic.compute_subsolar_point(et))
        return np.array([spice.generic.compute_subsolar_point(et)[1]])

    dataset_name = 'sub_solar_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [E]'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_spacecraft_latitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.generic.compute_subspacecraft_point(et)[0]])

    dataset_name = 'sub_spacecraft_latitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [N]'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_spacecraft_longitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        print(spice.generic.compute_subspacecraft_point(et))
        return np.array([spice.generic.compute_subspacecraft_point(et)[1]])

    dataset_name = 'sub_spacecraft_longitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [E]'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_spacecraft_altitude(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.generic.compute_subspacecraft_altitude(et)])

    dataset_name = 'sub_spacecraft_altitude'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_spacecraft_local_time(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        longitude = data_file.file[f'{group_path}/sub_spacecraft_longitude'][:][0]
        return np.array([spice.generic.compute_subspacecraft_local_time(et, np.radians(longitude))])

    dataset_name = 'sub_spacecraft_local_time'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Hours'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mars_sun_distance(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        et = data_file.file[f'{group_path}/ephemeris_time'][:][0]
        return np.array([spice.generic.compute_mars_sun_distance(et)])

    dataset_name = 'mars_sun_distance'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km'
    comment = 'Computed with SPICE.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_sub_solar_spacecraft_angle(data_file, group_path: str) -> None:
    def get_data() -> np.ndarray:
        sub_solar_latitude = data_file.file[f'{group_path}/sub_solar_latitude'][:][0]
        sub_solar_longitude = data_file.file[f'{group_path}/sub_solar_longitude'][:][0]
        sub_spacecraft_latitude = data_file.file[f'{group_path}/sub_spacecraft_latitude'][:][0]
        sub_spacecraft_longitude = data_file.file[f'{group_path}/sub_spacecraft_longitude'][:][0]
        return np.array([haversine(sub_solar_latitude, sub_solar_longitude, sub_spacecraft_latitude, sub_spacecraft_longitude)])

    dataset_name = 'sub_solar_spacecraft_angle'
    dataset_version_name = f'apsis_{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'Computed with my own haversine function.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path, latest_version):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment
