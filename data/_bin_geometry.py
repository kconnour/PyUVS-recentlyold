import h5py
import numpy as np

from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, hdulist, add_dimension_if_necessary


def add_latitude(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_lat'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'latitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [N]'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_lat structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_longitude(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_lon'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'longitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees [E]'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_lon structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_tangent_altitude(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'tangent_altitude'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_mrh_alt structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_tangent_altitude_rate(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt_rate'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'tangent_altitude_rate'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km/s'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_mrh_alt_rate structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_line_of_sight(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_los'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'line_of_sight'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'km'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_los structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_solar_zenith_angle(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_solar_zenith_angle'], 2) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'solar_zenith_angle'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_solar_zenith_angle structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_emission_angle(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_emission_angle'], 2) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'emission_angle'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_emission_angle structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_phase_angle(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_phase_angle'], 2) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'phase_angle'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_phase_angle structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_zenith_angle(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_phase_angle'], 2) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'zenith_angle'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_zenith_angle structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_local_time(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_local_time'], 2) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'local_time'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'hours'
    comment = 'This data is taken from the pixelgeometry/pixel_local_time structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_right_ascension(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_ra'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'right_ascension'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_ra structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_declination(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_corner_dec'], 3) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'declination'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the pixelgeometry/pixel_corner_dec structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_pixel_vector(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([add_dimension_if_necessary(f['pixelgeometry'].data['pixel_vec'], 4) for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'pixel_vector'
    dataset_version_name = f'{dataset_name}'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Unit vector'
    comment = 'This data is taken from the pixelgeometry/pixel_vec structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment
