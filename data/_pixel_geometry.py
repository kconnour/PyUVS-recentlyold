import numpy as np

from _structure import DataFile
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, hdulist


def add_latitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_corner_lat'] for f in hduls])

    dataset_name = 'latitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_lat structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_longitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_corner_lon'] for f in hduls])

    dataset_name = 'longitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_lon structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_tangent_altitude(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_corner_mrh_alt'] for f in hduls])

    dataset_name = 'tangent_altitude'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'km'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_mrh_alt structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_solar_zenith_angle(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_solar_zenith_angle'] for f in hduls])

    dataset_name = 'solar_zenith_angle'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_solar_zenith_angle structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_emission_angle(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_emission_angle'] for f in hduls])

    dataset_name = 'emission_angle'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_emission_angle structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_phase_angle(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_phase_angle'] for f in hduls])

    dataset_name = 'phase_angle'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_phase_angle structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_local_time(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['pixelgeometry'].data['pixel_local_time'] for f in hduls])

    dataset_name = 'local_time'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'hours'
    comment = 'This data is taken from the pixelgeometry/pixel_local_time structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment
