import warnings

import h5py
import numpy as np

import pyuvs as pu


compression = 'gzip'
compression_opts = 4


def add_channel_independent_integration_data_to_file(file: h5py.File, integration_path: str, hduls: pu.typing.hdulist) -> None:
    add_ephemeris_time(file, integration_path, hduls)
    add_field_of_view(file, integration_path, hduls)
    add_mirror_data_number(file, integration_path, hduls)
    add_case_temperature(file, integration_path, hduls)
    add_integration_time(file, integration_path, hduls)
    add_data_file(file, integration_path, hduls)
    add_swath_number(file, integration_path)
    add_opportunity_classification(file, integration_path)


def add_ephemeris_time(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'ephemeris_time'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Seconds since J2000'
    comment = 'This data is taken from the integration/et structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_field_of_view(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['fov_deg'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'field_of_view'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the integration/fov_deg structure of the v13 IUVS data. ' \
              'The field of view is simply double the mirror angle.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mirror_data_number(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'mirror_data_number'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'DN'
    comment = 'This data is taken from the integration/mirror_dn structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_case_temperature(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'case_temperature'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/case_temp_c structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_integration_time(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = pu.file_classification.get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['int_time'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'integration_time'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Seconds'
    comment = 'This data is from the observation/int_time structure of the v13 IUVS data.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_data_file(file: h5py.File, group_path: str, hduls: pu.typing.hdulist) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = pu.file_classification.get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(c, integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'data_file'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    unit = ''
    comment = 'This is the file index corresponding to each integration.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_swath_number(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        """Make the swath number associated with each mirror angle.

        This function assumes the input is all the mirror angles (or, equivalently,
        the field of view) from an orbital segment. Omitting some mirror angles
        may result in nonsensical results. Adding additional mirror angles from
        multiple segments or orbits will certainly result in nonsensical results.

        Returns
        -------
        np.ndarray
            The swath number associated with each mirror angle.

        Notes
        -----
        This algorithm assumes the mirror in roughly constant step sizes except
        when making a swath jump. It finds the median step size and then uses
        this number to find swath discontinuities. It interpolates between these
        indices and takes the floor of these values to get the integer swath
        number.

        """
        mirror_angles = file[f'{group_path}/field_of_view'][:]
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            mirror_change = np.diff(mirror_angles)
            threshold = np.abs(np.median(mirror_change)) * 4
            mirror_discontinuities = np.where(np.abs(mirror_change) > threshold)[0] + 1
            if any(mirror_discontinuities):
                n_swaths = len(mirror_discontinuities) + 1
                integrations = range(len(mirror_angles))
                interp_swaths = np.interp(integrations, mirror_discontinuities, range(1, n_swaths), left=0)
                return np.floor(interp_swaths).astype('int')
            else:
                return np.zeros(mirror_angles.shape)

    dataset_name = 'swath_number'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'The number of each swath in the observation.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_opportunity_classification(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        swath_number = file[f'{group_path}/swath_number'][:]
        field_of_view = file[f'{group_path}/field_of_view'][:]

        relay_integrations = np.empty(swath_number.shape, dtype='bool')
        for sn in np.unique(swath_number):
            angles = field_of_view[swath_number == sn]
            relay = pu.constants.minimum_mirror_angle * 2 in angles and pu.constants.maximum_mirror_angle * 2 in angles
            relay_integrations[swath_number == sn] = relay
        return relay_integrations

    dataset_name = 'opportunity'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_version = pu.data_versions.get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration is part of a opportunistic swath; False otherwise.'

    if not pu.data_versions.dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data(), compression=compression, compression_opts=compression_opts)
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not pu.data_versions.current_dataset_is_up_to_date(file, dataset_path, latest_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
