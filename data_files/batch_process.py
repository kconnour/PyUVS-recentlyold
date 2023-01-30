import math
from pathlib import Path

from astropy.io import fits
import h5py

'''from _apsis import add_apsis_data_to_file
from _binning import add_binning_data_to_file
from _integration import add_channel_independent_integration_data_to_file, add_channel_dependent_integration_data_to_file
from _miscellaneous import get_opportunity_file_indices, get_failsafe_file_indices, get_dayside_file_indices
from _pixel_geometry import add_pixel_geometry_data_to_file
from _spacecraft_geometry import add_spacecraft_geometry_data_to_file'''
import apoapse
import pyuvs as pu


def make_orbit_block(orbit: int) -> str:
    block = math.floor(orbit / 100) * 100
    return 'orbit' + f'{block}'.zfill(5)


def make_orbit_code(orbit: int) -> str:
    return 'orbit' + f'{orbit}'.zfill(5)


def make_hdf5_filename(orbit: int, save_location: Path) -> Path:
    filename = f'{make_orbit_code(orbit)}.hdf5'
    return save_location / make_orbit_block(orbit) / filename


def open_latest_file(filepath: Path) -> h5py.File:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        f = h5py.File(filepath, mode='x')  # 'x' means to create the file but fail if it already exists
    except FileExistsError:
        f = h5py.File(filepath, mode='r+')  # 'r+' means read/write and file must exist
    return f


def create_file(orbit: int) -> h5py.File:
    hdf5_filename = make_hdf5_filename(orbit, data_file_save_location)
    file = open_latest_file(hdf5_filename)
    if 'orbit' not in file.attrs.keys():
        file.attrs['orbit'] = orbit
    return file


if __name__ == '__main__':
    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    for orbit in range(2893, 2894):
        print(orbit)
        orbit_block = make_orbit_block(orbit)
        orbit_code = make_orbit_code(orbit)
        file = create_file(orbit)
        # TODO: if overall data product number is up to date, skip the below to not overwrite it

        for segment in ['apoapse']:
            apoapse_path = 'apoapse'
            file.require_group(apoapse_path)

            match segment:
                case 'apoapse':
                    apoapse_apsis_path = 'apoapse/apsis'
                    file.require_group(apoapse_apsis_path)
                    apoapse.apsis.add_apsis_data_to_file(file, apoapse_apsis_path, None)

                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                    hduls = [fits.open(f) for f in data_files]

                    apoapse_integration_path = 'apoapse/integration'
                    file.require_group(apoapse_integration_path)
                    apoapse.integration.add_channel_independent_integration_data_to_file(file, apoapse_integration_path, hduls)

                    apoapse_spacecraft_geometry_path = 'apoapse/spacecraft_geometry'
                    file.require_group(apoapse_spacecraft_geometry_path)
                    apoapse.spacecraft_geometry.add_spacecraft_geometry_data_to_file(file, apoapse_spacecraft_geometry_path, apoapse_path, hduls)

                    apoapse_pixel_geometry_path = 'apoapse/pixel_geometry'
                    file.require_group(apoapse_pixel_geometry_path)
                    apoapse.pixel_geometry.add_pixel_geometry_data_to_file(file, apoapse_pixel_geometry_path)

                    for channel in ['muv']:
                        match channel:
                            case 'muv':
                                apoapse_muv_path = f'apoapse/muv'
                                file.require_group(apoapse_muv_path)
                                # Get the data files for this channel
                                apoapse_muv_data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                                apoapse_muv_hduls = [fits.open(f) for f in apoapse_muv_data_files]

                                # Classify hduls
                                failsafe_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_failsafe_files(apoapse_muv_hduls)[c]]
                                dayside_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_dayside_files(apoapse_muv_hduls)[c]
                                                     and f not in failsafe_hduls]
                                nightside_hduls = [f for f in apoapse_muv_hduls if f not in failsafe_hduls and f not in dayside_hduls]

                                apoapse_muv_integration_path = 'apoapse/muv/integration'
                                file.require_group(apoapse_muv_integration_path)
                                apoapse.muv.integration.add_channel_dependent_integration_data_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)

                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    match experiment:
                                        case 'failsafe':
                                            apoapse_muv_failsafe_path = 'apoapse/muv/failsafe'
                                            file.require_group(apoapse_muv_failsafe_path)

                                            apoapse_muv_failsafe_binning_path = 'apoapse/muv/failsafe/binning'
                                            file.require_group(apoapse_muv_failsafe_binning_path)
                                            apoapse.muv.failsafe.binning.add_binning_data_to_file(file, apoapse_muv_failsafe_binning_path, failsafe_hduls)

                                            apoapse_muv_failsafe_detector_path = 'apoapse/muv/failsafe/detector'
                                            file.require_group(apoapse_muv_failsafe_detector_path)
                                            # TODO: this

                                            apoapse_muv_failsafe_bin_geometry_path = 'apoapse/muv/failsafe/bin_geometry'
                                            file.require_group(apoapse_muv_failsafe_bin_geometry_path)
                                            apoapse.muv.failsafe.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_failsafe_bin_geometry_path, 'apoapse', failsafe_hduls)

                                        case 'dayside':
                                            apoapse_muv_dayside_path = 'apoapse/muv/dayside'
                                            file.require_group(apoapse_muv_dayside_path)

                                            apoapse_muv_dayside_binning_path = 'apoapse/muv/dayside/binning'
                                            file.require_group(apoapse_muv_dayside_binning_path)
                                            apoapse.muv.dayside.binning.add_binning_data_to_file(file, apoapse_muv_dayside_binning_path, dayside_hduls)

                                            apoapse_muv_dayside_detector_path = 'apoapse/muv/dayside/detector'
                                            file.require_group(apoapse_muv_dayside_detector_path)
                                            # TODO: data

                                            apoapse_muv_dayside_bin_geometry_path = 'apoapse/muv/dayside/bin_geometry'
                                            file.require_group(apoapse_muv_dayside_bin_geometry_path)
                                            apoapse.muv.dayside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_dayside_bin_geometry_path, 'apoapse', dayside_hduls)

                                        case 'nightside':
                                            apoapse_muv_nightside_path = 'apoapse/muv/nightside'
                                            file.require_group(apoapse_muv_nightside_path)

                                            apoapse_muv_nightside_binning_path = 'apoapse/muv/nightside/binning'
                                            file.require_group(apoapse_muv_nightside_binning_path)
                                            apoapse.muv.nightside.binning.add_binning_data_to_file(file, apoapse_muv_nightside_binning_path, nightside_hduls)

                                            apoapse_muv_nightside_detector_path = 'apoapse/muv/nightside/detector'
                                            file.require_group(apoapse_muv_nightside_detector_path)
                                            # TODO: data

                                            apoapse_muv_nightside_bin_geometry_path = 'apoapse/muv/nightside/bin_geometry'
                                            file.require_group(apoapse_muv_nightside_bin_geometry_path)
                                            apoapse.muv.nightside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_nightside_bin_geometry_path, 'apoapse', nightside_hduls)
