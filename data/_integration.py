from pathlib import Path

import numpy as np

from constants import minimum_mirror_angle, maximum_mirror_angle, day_night_voltage_boundary
from _structure import DataFile
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, get_integrations_per_file, hdulist


def add_ephemeris_time(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_ephemeris_time() -> np.ndarray:
        return np.concatenate([f['integration'].data['et'] for f in hduls])

    dataset_name = 'ephemeris_time'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Seconds since J2000'
    comment = 'This data is taken from the integration/et structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_ephemeris_time())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_ephemeris_time()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_field_of_view(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_field_of_view() -> np.ndarray:
        return np.concatenate([f['integration'].data['fov_deg'] for f in hduls])

    dataset_name = 'field_of_view'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees'
    comment = 'This data is taken from the integration/fov_deg structure of the v13 IUVS data. Also, this array is simply' \
              'double the mirror angle.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_field_of_view())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_field_of_view()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_mirror_data_number(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_mirror_data_number() -> np.ndarray:
        return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls])

    dataset_name = 'mirror_data_number'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'DN'
    comment = 'This data is taken from the integration/mirror_dn structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_mirror_data_number())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_mirror_data_number()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_detector_temperature(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_detector_temperature() -> np.ndarray:
        return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls])

    dataset_name = 'detector_temperature'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/det_temp_c structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_detector_temperature())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_detector_temperature()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_case_temperature(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_case_temperature() -> np.ndarray:
        return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls])

    dataset_name = 'case_temperature'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Degrees C'
    comment = 'This data is taken from the integration/case_temp_c structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_case_temperature())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_case_temperature()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_integration_time(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_integration_time() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['int_time'], integrations_per_file[c]) for c, f in enumerate(hduls)])

    dataset_name = 'integration_time'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    comment = 'This data is from the observation/int_time structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_integration_time())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_integration_time()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_swath_number(data_file: DataFile, group_path: str) -> None:
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
    dataset_path = make_dataset_path(group_path, dataset_name)
    last_validated_orbit = get_latest_pipeline_versions()['last_validated_orbit']
    comment = 'The number of each swath in the observation.'
    orbit = data_file.file.attrs['orbit']

    if not dataset_exists(data_file, dataset_path):
        swath_number = determine_swath_number(data_file.file[f'{group_path}/field_of_view'][:])
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=swath_number)
        dataset.attrs['last_validated_orbit'] = last_validated_orbit
        dataset.attrs['comment'] = comment
        data_file.file[group_path].attrs['swaths'] = swath_number[-1] + 1

    elif data_file.file[dataset_path].attrs['last_validated_orbit'] < last_validated_orbit:
        caveat = np.genfromtxt(Path(__file__).resolve().parent / 'swath_caveat.csv', skip_header=1, delimiter=',')
        dataset = data_file.file[dataset_path]
        if orbit in caveat[:, 0]:
            row_index = np.argmax(caveat[:, 0] == orbit)
            dataset[:] = determine_swath_number(data_file.file[f'{group_path}/field_of_view'][:]) + caveat[row_index, 1]
            dataset.attrs['last_validated_orbit'] = last_validated_orbit
            dataset.attrs['comment'] = comment
            data_file.file[group_path].attrs['swaths'] = caveat[row_index, 2]
        else:
            dataset.attrs['last_validated_orbit'] = last_validated_orbit


def add_relay_classification(data_file: DataFile, group_path: str) -> None:
    def get_relay_integrations() -> np.ndarray:
        swath_number = data_file.file[f'{group_path}/swath_number'][:]
        field_of_view = data_file.file[f'{group_path}/field_of_view'][:]

        relay_integrations = np.empty(swath_number.shape, dtype='bool')
        for sn in np.unique(swath_number):
            angles = field_of_view[swath_number == sn]
            relay = minimum_mirror_angle * 2 in angles and maximum_mirror_angle * 2 in angles
            relay_integrations[swath_number == sn] = relay
        return relay_integrations

    dataset_name = 'relay'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    comment = 'True if the integration is part of a relay swath; False otherwise.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_relay_integrations())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_relay_integrations()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_voltage(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_voltage() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_volt'], integrations_per_file[c]) for c, f in enumerate(hduls)])

    dataset_name = 'voltage'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    comment = 'This data is taken from the observation/mcp_volt structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_voltage())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = 'Volts'
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_voltage()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment


def add_voltage_gain(data_file: DataFile, group_path: str, hduls: list[hdulist]) -> None:
    def get_voltage_gain() -> np.ndarray:
        integrations_per_file = get_integrations_per_file(hduls)
        return np.concatenate([np.repeat(f['observation'].data['mcp_gain'], integrations_per_file[c]) for c, f in enumerate(hduls)])

    dataset_name = 'voltage_gain'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'Volts'
    comment = 'This data is taken from the observation/mcp_gain structure of the v13 IUVS data.'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_voltage_gain())
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_voltage_gain()
        dataset.attrs['version'] = latest_version
        dataset.attrs['unit'] = unit
        dataset.attrs['comment'] = comment


def add_dayside_integrations(data_file: DataFile, group_path: str) -> None:
    def get_dayside_integrations() -> np.ndarray:
        voltage: np.ndarray = data_file.file[f'{group_path}/voltage'][:]
        return voltage < day_night_voltage_boundary

    dataset_name = 'dayside'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    comment = 'True if dayside; False if nightside. Derived from engineering settings of observation/mcp_gain'

    if not dataset_exists(data_file, dataset_path):
        dataset = data_file.file[group_path].create_dataset(dataset_name, data=get_dayside_integrations())
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment

    elif not current_dataset_is_up_to_date(data_file, dataset_path):
        dataset = data_file.file[dataset_path]
        dataset[:] = get_dayside_integrations()
        dataset.attrs['version'] = latest_version
        dataset.attrs['comment'] = comment
