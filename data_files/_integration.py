from pathlib import Path
import warnings

import h5py
import numpy as np

from constants import minimum_mirror_angle, maximum_mirror_angle, day_night_voltage_boundary
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import get_integrations_per_file, hdulist


def add_channel_independent_integration_data_to_file(file: h5py.File, integration_path: str, hduls: list[hdulist]) -> None:
    add_ephemeris_time(file, integration_path, hduls)
    add_field_of_view(file, integration_path, hduls)
    add_mirror_data_number(file, integration_path, hduls)
    add_case_temperature(file, integration_path, hduls)
    add_integration_time(file, integration_path, hduls)
    add_swath_number(file, integration_path)
    add_relay_classification(file, integration_path)


def add_channel_dependent_integration_data_to_file(file: h5py.File, integration_path: str, hduls: list[hdulist]) -> None:
    add_detector_temperature(file, integration_path, hduls)
    add_voltage(file, integration_path, hduls)
    add_voltage_gain(file, integration_path, hduls)


def add_ephemeris_time(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'ephemeris_time'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Seconds since J2000'
    comment = 'This data is taken from the integration/et structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_field_of_view(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['fov_deg'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'field_of_view'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees'
    comment = 'This data is taken from the integration/fov_deg structure of the v13 IUVS data. ' \
              'The field of view is simply double the mirror angle.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mirror_data_number(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'mirror_data_number'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'DN'
    comment = 'This data is taken from the integration/mirror_dn structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_detector_temperature(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'detector_temperature'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/det_temp_c structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_case_temperature(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls]) if hduls else np.array([])

    dataset_name = 'case_temperature'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/case_temp_c structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_integration_time(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['int_time'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'integration_time'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Seconds'
    comment = 'This data is from the observation/int_time structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_swath_number(file: h5py.File, group_path: str) -> None:
    def determine_swath_number(mirror_angles: np.ndarray) -> np.ndarray:
        """Make the swath number associated with each mirror angle.

        This function assumes the input is all the mirror angles (or, equivalently,
        the field of view) from an orbital segment. Omitting some mirror angles
        may result in nonsensical results. Adding additional mirror angles from
        multiple segments or orbits will certainly result in nonsensical results.

        Parameters
        ----------
        mirror_angles: np.ndarray
            1D array of the mirror angles from an orbital segment.

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

    def get_n_swaths(swath_numbers: np.ndarray) -> int:
        try:
            return swath_numbers[-1] + 1
        except IndexError:
            return 0

    dataset_name = 'swath_number'
    dataset_path = f'{group_path}/{dataset_name}'
    last_validated_orbit = get_latest_pipeline_versions()['last_validated_orbit']
    comment = 'The number of each swath in the observation.'
    orbit = file.attrs['orbit']

    # If it doesn't exist, it should always be larger than the last validated orbit. Cause if not, how would it be validated?
    if not dataset_exists(file, dataset_path):
        swath_number = determine_swath_number(file[f'{group_path}/field_of_view'][:])
        dataset = file[group_path].create_dataset(dataset_name, data=swath_number)
        dataset.attrs['last_validated_orbit'] = last_validated_orbit
        dataset.attrs['comment'] = comment
        file[group_path].attrs['swaths'] = get_n_swaths(swath_number)

    elif file[dataset_path].attrs['last_validated_orbit'] < orbit <= last_validated_orbit:
        caveat = np.genfromtxt(Path(__file__).resolve().parent / 'swath_caveat.csv', skip_header=1, delimiter=',')
        dataset = file[dataset_path]
        row_index = np.argmax(caveat[:, 0] == orbit)
        record = caveat[row_index]
        if not np.isnan(record[1]):
            dataset[:] = determine_swath_number(file[f'{group_path}/field_of_view'][:]) + record[1]
        if not np.isnan(record[2]):
            file[group_path].attrs['swaths'] = record[2]
        dataset.attrs['last_validated_orbit'] = last_validated_orbit
        dataset.attrs['comment'] = comment


def add_relay_classification(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        swath_number = file[f'{group_path}/swath_number'][:]
        field_of_view = file[f'{group_path}/field_of_view'][:]

        relay_integrations = np.empty(swath_number.shape, dtype='bool')
        for sn in np.unique(swath_number):
            angles = field_of_view[swath_number == sn]
            relay = minimum_mirror_angle * 2 in angles and maximum_mirror_angle * 2 in angles
            relay_integrations[swath_number == sn] = relay
        return relay_integrations

    dataset_name = 'relay'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if the integration is part of a relay swath; False otherwise.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['comment'] = comment


def add_voltage(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_volt'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'voltage'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Volts'
    comment = 'This data is taken from the observation/mcp_volt structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_voltage_gain(file: h5py.File, group_path: str, hduls: list[hdulist]) -> None:
    def get_data() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_gain'], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])

    dataset_name = 'voltage_gain'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    unit = 'Volts'
    comment = 'This data is taken from the observation/mcp_gain structure of the v13 IUVS data.'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_dayside_integrations(file: h5py.File, group_path: str) -> None:
    def get_data() -> np.ndarray:
        voltage: np.ndarray = file[f'{group_path}/voltage'][:]
        return voltage < day_night_voltage_boundary

    dataset_name = 'dayside'
    dataset_version_name = f'{dataset_name}'
    dataset_path = f'{group_path}/{dataset_name}'
    latest_pipeline_version = get_latest_pipeline_versions()[dataset_version_name]
    comment = 'True if dayside; False if nightside. Derived from engineering settings of observation/mcp_gain'

    if not dataset_exists(file, dataset_path):
        dataset = file[group_path].create_dataset(dataset_name, data=get_data())
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(file, dataset_path, latest_pipeline_version):
        dataset = file[dataset_path]
        dataset[:] = get_data()
        dataset.attrs['version'] = latest_pipeline_version
        dataset.attrs['comment'] = comment
