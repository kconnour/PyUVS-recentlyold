from datetime import datetime
from pathlib import Path

from astropy.io import fits

from _file_setup import create_file, add_basic_attributes_to_file
import apoapse
import pyuvs as pu


if __name__ == '__main__':
    version: int = 1

    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    pu.spice.clear_existing_kernels()
    pu.spice.furnish_standard_kernels(spice_kernel_location)
    # TODO: See if I can compute the latest datetime of the kernels I have and use that
    apoapsis_orbits, approximate_apoapsis_ephemeris_times = pu.spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2019, 1, 1), step_size=60)

    for orbit in range(4000, 4001):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)
        try:
            file = create_file(orbit, version, data_file_save_location)
        except FileExistsError:
            continue
        add_basic_attributes_to_file(file, orbit, version)

        for segment in ['apoapse']:
            file.create_group(f'{segment}')

            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*apoapse*{orbit_code}*muv*.gz'))
                    hduls = [fits.open(f) for f in data_files]

                    file.create_group('apoapse/apsis')
                    apoapse.apsis.add_apsis_data_to_file(file, approximate_apoapsis_ephemeris_times)

                    file.create_group('apoapse/integration')
                    apoapse.integration.add_channel_independent_integration_data_to_file(file, hduls)

                    file.create_group('apoapse/spacecraft_geometry')
                    apoapse.spacecraft_geometry.add_spacecraft_geometry_data_to_file(file, hduls)

                    file.create_group('apoapse/pixel_geometry')
                    apoapse.pixel_geometry.add_pixel_geometry_data_to_file(file)

                    for channel in ['muv']:
                        file.create_group(f'{segment}/{channel}')

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

                                file.create_group('apoapse/muv/integration')
                                apoapse.muv.integration.add_channel_dependent_integration_data_to_file(file, apoapse_muv_hduls)

                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    file.create_group(f'{segment}/{channel}/{experiment}')

                                    match experiment:
                                        case 'failsafe':
                                            file.create_group('apoapse/muv/failsafe/binning')
                                            apoapse.muv.failsafe.binning.add_binning_data_to_file(file, failsafe_hduls)

                                            file.create_group('apoapse/muv/failsafe/detector')

                                            file.create_group('apoapse/muv/failsafe/bin_geometry')
                                            #apoapse.muv.failsafe.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_failsafe_bin_geometry_path, 'apoapse', failsafe_hduls)

                                        case 'dayside':
                                            file.create_group('apoapse/muv/dayside/binning')
                                            apoapse.muv.dayside.binning.add_binning_data_to_file(file, dayside_hduls)

                                            file.create_group('apoapse/muv/dayside/detector')

                                            file.create_group('apoapse/muv/dayside/bin_geometry')
                                            #apoapse.muv.dayside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_dayside_bin_geometry_path, 'apoapse', dayside_hduls)

                                        case 'nightside':
                                            file.create_group('apoapse/muv/nightside/binning')
                                            apoapse.muv.nightside.binning.add_binning_data_to_file(file, nightside_hduls)

                                            file.create_group('apoapse/muv/nightside/detector')

                                            file.create_group('apoapse/muv/nightside/bin_geometry')
                                            #apoapse.muv.nightside.bin_geometry.add_bin_geometry_data_to_file(file, apoapse_muv_nightside_bin_geometry_path, 'apoapse', nightside_hduls)
