import warnings

import h5py
import numpy as np

from constants import pixel_angular_size
from _anc import load_muv_flatfield, load_muv_sensitivity_curve_observational, load_voltage_correction_voltage, load_voltage_correction_coefficients
from _data_versions import current_dataset_is_up_to_date, get_latest_pipeline_versions, dataset_exists
from _miscellaneous import make_dataset_path, hdulist


warnings.filterwarnings('ignore')


def add_raw(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([f['detector_raw'].data for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'raw'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'DN'
    comment = 'This data is taken from the detector_raw structure of the v13 IUVS data.'

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


def add_dark_subtracted(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str) -> None:
    def get_data() -> np.ndarray:
        if hduls:
            data = np.concatenate([f['detector_dark_subtracted'].data for f in hduls])
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'dark_subtracted'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'DN'
    comment = 'This data is taken from the detector_dark_subtracted structure of the v13 IUVS data.'

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


def add_brightness(file: h5py.File, group_path: str, hduls: list[hdulist], segment_path: str, binning_path: str, time_path: str, voltage_path: str, daynight: bool) -> None:
    def make_flatfield(
            spatial_bin_edges: np.ndarray,
            spectral_bin_edges: np.ndarray) -> np.ndarray:
        """Make the flatfield for a given binning configuration.

        This function will rebin the "master" 133x19 flatfield constructed from
        data during the MY34 GDS onto the given spatial and spectral binning
        scheme.

        Parameters
        ----------
        spatial_bin_edges
            Spatial bin edges. This argument should be an array of integers.
        spectral_bin_edges
            Spectral bin edges. This argument should be an array of integers.

        Returns
        -------
        np.ndarray
            The flatfield for the given binning scheme.

        """
        # The data from which the flatfield was made had the following properties:
        # spatial: started pixel 103, ended on 901, and had a width of 6 pixels
        # spectra: started pixel 172, ended on 818, and had a width of 34 pixels
        original_ff = load_muv_flatfield()
        ff_expanded = np.repeat(np.repeat(original_ff, 6, axis=0), 34, axis=1)
        ff1024 = np.pad(ff_expanded, ((103, 1024 - 901), (172, 1024 - 818)), mode='edge')

        spatial_bins = spatial_bin_edges.shape[0] - 1
        spectral_bins = spectral_bin_edges.shape[0] - 1

        new_flatfield = np.zeros((spatial_bins, spectral_bins))
        for spatial_bin in range(spatial_bins):
            for spectral_bin in range(spectral_bins):
                new_flatfield[spatial_bin, spectral_bin] = np.mean(
                    ff1024[spatial_bin_edges[spatial_bin]: spatial_bin_edges[spatial_bin + 1],
                    spectral_bin_edges[spectral_bin]: spectral_bin_edges[spectral_bin + 1]])
        return new_flatfield

    def make_gain_correction(det_dark_subtracted, spa_size, spe_size, int_time, mcp_volt, mcp_gain):
        """

        Parameters
        ----------
        dds: np.ndarray
            The detector dark subtacted
        spa_size: int
            The number of detector pixels in a spatial bin
        spe_size: int
            The number of detector pixels in a spectral bin
        integration_time
        mcp_volt
        mcp_gain

        Returns
        -------

        """
        volt_array = load_voltage_correction_voltage()
        ab = load_voltage_correction_coefficients()
        ref_mcp_gain = 50.909455

        normalized_img = det_dark_subtracted.T / int_time / spa_size / spe_size

        a = np.interp(mcp_volt, volt_array, ab[:, 0])
        b = np.interp(mcp_volt, volt_array, ab[:, 1])

        norm_img = np.exp(a + b * np.log(normalized_img))
        return (norm_img / normalized_img * mcp_gain / ref_mcp_gain).T

    def get_data() -> np.ndarray:
        if hduls:
            daynight_integrations = file[f'{voltage_path}/dayside'][:] == daynight

            detector_dark_subtracted = file[f'{group_path}/dark_subtracted'][:]
            spatial_bin_edges_ds = file[f'{binning_path}/spatial_bin_edges']
            spatial_bin_edges = spatial_bin_edges_ds[:]
            spatial_bin_width = spatial_bin_edges_ds.attrs['width']
            spectral_bin_edges_ds = file[f'{binning_path}/spectral_bin_edges']
            spectral_bin_edges = spectral_bin_edges_ds[:]
            spectral_bin_width = spectral_bin_edges_ds.attrs['width']
            integration_time = file[f'{time_path}/integration_time'][:][daynight_integrations]
            voltage = file[f'{voltage_path}/voltage'][:][daynight_integrations]
            voltage_gain = file[f'{voltage_path}/voltage_gain'][:][daynight_integrations]

            flatfield = make_flatfield(spatial_bin_edges, spectral_bin_edges)
            sensitivity_curve = load_muv_sensitivity_curve_observational()[:, 1]

            # Make the sensitivity curve 1024 elements for simplicity
            sensitivity_curve = np.repeat(sensitivity_curve, 2)

            # Get the sensitivity in each spectral bin
            # For array shape reasons, I spread this out over several lines
            rebinned_sensitivity_curve = np.array([np.mean(sensitivity_curve[spectral_bin_edges[i]:spectral_bin_edges[i+1]]) for i in range(spectral_bin_edges.shape[0] - 1)])
            partial_corrected_brightness = detector_dark_subtracted / rebinned_sensitivity_curve * 4 * np.pi * 10**-9 / pixel_angular_size / spatial_bin_width
            partial_corrected_brightness = (partial_corrected_brightness.T / voltage_gain / integration_time).T

            # Hypothetically these are good, but in reality they need flatfield and voltage corrections
            voltage_correction = make_gain_correction(detector_dark_subtracted, spatial_bin_width, spectral_bin_width, integration_time, voltage, voltage_gain)
            data = partial_corrected_brightness / flatfield * voltage_correction
            app_flip = file[f'{segment_path}/app_flip'][:][0]
            data = np.fliplr(data) if app_flip else data
        else:
            data = np.array([])
        return data

    dataset_name = 'brightness'
    dataset_path = make_dataset_path(group_path, dataset_name)
    latest_version = get_latest_pipeline_versions()[dataset_name]
    unit = 'kR'
    comment = 'This data is created myself. It ignores the v13 primary.'

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
