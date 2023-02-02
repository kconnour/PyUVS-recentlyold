import math
from pathlib import Path

from astropy.io import fits
import h5py

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

    # TODO: get approximate ephemeris times here

    for orbit in range(100, 200):
        print(orbit)
        orbit_block = make_orbit_block(orbit)
        orbit_code = make_orbit_code(orbit)
        file = create_file(orbit)
        # TODO: if overall data product number is up to date, skip the below to not overwrite it

        for segment in ['apoapse']:
            file.require_group(f'{segment}')

            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                    hduls = [fits.open(f) for f in data_files]

                    file.require_group('apoapse/apsis')
                    apoapse.apsis.add_apsis_data_to_file(file)

                    file.require_group('apoapse/integration')
                    apoapse.integration.add_channel_independent_integration_data_to_file(file, hduls)

                    file.require_group('apoapse/spacecraft_geometry')
                    apoapse.spacecraft_geometry.add_spacecraft_geometry_data_to_file(file, hduls)

                    file.require_group('apoapse/pixel_geometry')
                    apoapse.pixel_geometry.add_pixel_geometry_data_to_file(file)

                    for channel in ['muv']:
                        file.require_group(f'{segment}/{channel}')

                        match channel:
                            case 'muv':
                                # Get the data files for this channel
                                apoapse_muv_data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                                apoapse_muv_hduls = [fits.open(f) for f in apoapse_muv_data_files]

                                # Classify hduls
                                failsafe_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_apoapse_muv_failsafe_files(apoapse_muv_hduls)[c]]
                                dayside_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_apoapse_muv_dayside_files(apoapse_muv_hduls)[c]
                                                     and f not in failsafe_hduls]
                                nightside_hduls = [f for f in apoapse_muv_hduls if f not in failsafe_hduls and f not in dayside_hduls]

                                file.require_group('apoapse/muv/integration')
                                apoapse.muv.integration.add_channel_dependent_integration_data_to_file(file, apoapse_muv_hduls)

                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    file.require_group(f'{segment}/{channel}/{experiment}')

                                    match experiment:
                                        case 'failsafe':
                                            file.require_group('apoapse/muv/failsafe/binning')
                                            apoapse.muv.failsafe.binning.add_binning_data_to_file(file, failsafe_hduls)

                                            file.require_group('apoapse/muv/failsafe/detector')

                                            file.require_group('apoapse/muv/failsafe/bin_geometry')
                                            #apoapse.muv.failsafe.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_failsafe_bin_geometry_path, 'apoapse', failsafe_hduls)

                                        case 'dayside':
                                            file.require_group('apoapse/muv/dayside/binning')
                                            apoapse.muv.dayside.binning.add_binning_data_to_file(file, dayside_hduls)

                                            file.require_group('apoapse/muv/dayside/detector')

                                            file.require_group('apoapse/muv/dayside/bin_geometry')
                                            #apoapse.muv.dayside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_dayside_bin_geometry_path, 'apoapse', dayside_hduls)

                                        case 'nightside':
                                            file.require_group('apoapse/muv/nightside/binning')
                                            apoapse.muv.nightside.binning.add_binning_data_to_file(file, nightside_hduls)

                                            file.require_group('apoapse/muv/nightside/detector')

                                            file.require_group('apoapse/muv/nightside/bin_geometry')
                                            #apoapse.muv.nightside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_nightside_bin_geometry_path, 'apoapse', nightside_hduls)
