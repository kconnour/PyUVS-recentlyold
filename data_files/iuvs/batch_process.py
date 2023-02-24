from datetime import datetime
import multiprocessing as mp
from pathlib import Path

from astropy.io import fits

import pyuvs as pu
from file_setup import open_latest_file, add_orbit_attribute_to_file
from fits_sort import get_apoapse_muv_fits_files


if __name__ == '__main__':
    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data/development')
    iuvs_data_version: int = 13

    #pu.spice.clear_existing_kernels()
    #pu.spice.furnish_standard_kernels(spice_kernel_location)
    # TODO: See if I can compute the latest datetime of the kernels I have and use that
    # TODO: I don't know how to test this or structure code...
    # apoapsis_orbits, approximate_apoapsis_ephemeris_times = pu.spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2022, 9, 2), step_size=60)

    def batch_process_orbit(orbit: int) -> None:
        print(orbit)
        file = open_latest_file(orbit, data_file_save_location)
        add_orbit_attribute_to_file(file, orbit)

        for segment in ['apoapse']:
            file.require_group(f'{segment}')

            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    hduls = get_apoapse_muv_fits_files(iuvs_fits_file_location, orbit)

                    #file.create_group('apoapse/apsis')
                    #apoapse.apsis.add_apsis_data_to_file(file, approximate_apoapsis_ephemeris_times)

                    apoapse_integration_path = 'apoapse/integration'
                    file.require_group(apoapse_integration_path)
                    apoapse.integration.add_channel_independent_integration_data_to_file(file, hduls, orbit)
                    '''
                    file.create_group('apoapse/spacecraft_geometry')
                    apoapse.spacecraft_geometry.add_spacecraft_geometry_data_to_file(file, hduls)

                    for channel in ['muv']:
                        file.create_group(f'{segment}/{channel}')

                        match channel:
                            case 'muv':
                                # Get the data files for this channel
                                apoapse_muv_data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                                apoapse_muv_hduls = [fits.open(f) for f in apoapse_muv_data_files]

                                # Classify hduls
                                failsafe_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_apoapse_muv_failsafe_files(apoapse_muv_hduls, orbit)[c]]
                                dayside_hduls = [f for c, f in enumerate(apoapse_muv_hduls) if pu.file_classification.determine_apoapse_muv_dayside_files(apoapse_muv_hduls)[c]
                                                     and f not in failsafe_hduls]
                                nightside_hduls = [f for f in apoapse_muv_hduls if f not in failsafe_hduls and f not in dayside_hduls]

                                file.create_group('apoapse/muv/integration')
                                apoapse.muv.integration.add_channel_dependent_integration_data_to_file(file, apoapse_muv_hduls, orbit)

                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    file.create_group(f'{segment}/{channel}/{experiment}')

                                    match experiment:
                                        case 'failsafe':
                                            file.create_group('apoapse/muv/failsafe/binning')
                                            apoapse.muv.failsafe.binning.add_binning_data_to_file(file, failsafe_hduls)

                                            file.create_group('apoapse/muv/failsafe/detector')
                                            apoapse.muv.failsafe.detector.add_detector_data_to_file(file, failsafe_hduls)

                                            file.create_group('apoapse/muv/failsafe/bin_geometry')
                                            apoapse.muv.failsafe.bin_geometry.add_bin_geometry_data_to_file(file, failsafe_hduls)

                                        case 'dayside':
                                            file.create_group('apoapse/muv/dayside/binning')
                                            apoapse.muv.dayside.binning.add_binning_data_to_file(file, dayside_hduls)

                                            file.create_group('apoapse/muv/dayside/detector')
                                            apoapse.muv.dayside.detector.add_detector_data_to_file(file, dayside_hduls)

                                            file.create_group('apoapse/muv/dayside/bin_geometry')
                                            apoapse.muv.dayside.bin_geometry.add_bin_geometry_data_to_file(file, dayside_hduls)

                                        case 'nightside':
                                            file.create_group('apoapse/muv/nightside/binning')
                                            apoapse.muv.nightside.binning.add_binning_data_to_file(file, nightside_hduls)

                                            file.create_group('apoapse/muv/nightside/detector')
                                            apoapse.muv.nightside.detector.add_detector_data_to_file(file, nightside_hduls)

                                            file.create_group('apoapse/muv/nightside/bin_geometry')
                                            apoapse.muv.nightside.bin_geometry.add_bin_geometry_data_to_file(file, nightside_hduls)

                    # In theory, I should be able to do this above with SPICE kernels, but since I need the pixel vector
                    #  I'm doing it here
                    file.create_group('apoapse/pixel_geometry')
                    apoapse.pixel_geometry.add_pixel_geometry_data_to_file(file)
        file.close()

    n_cpus = mp.cpu_count()
    pool = mp.Pool(n_cpus - 1)

    for orb in range(3100, 4000):
        pool.apply_async(func=batch_process_orbit, args=(orb,))
        #batch_process_orbit(orb)
    pool.close()
    pool.join()'''
