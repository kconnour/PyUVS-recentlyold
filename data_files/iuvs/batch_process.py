from pathlib import Path

from file_setup import open_latest_file, add_orbit_attribute_to_file, add_version_attribute_to_file
from fits_sort import get_apoapse_muv_fits_files
import instrument_geometry as instrument_geometry
import integration as integration
import spacecraft_geometry as spacecraft_geometry


# Note: I absolutely cannot think of a way to version each array in a smart way. The code just gets out of control
# when thinking that I have to track all the dependencies of a change in the code. Assigning a singular version to the
# entire file is the only sensible solution I can think of

if __name__ == '__main__':
    version: int = 1

    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    #pu.spice.clear_existing_kernels()
    #pu.spice.furnish_standard_kernels(spice_kernel_location)
    # TODO: See if I can compute the latest datetime of the kernels I have and use that
    # TODO: I don't know how to test this or structure code...
    # apoapsis_orbits, approximate_apoapsis_ephemeris_times = pu.spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2022, 9, 2), step_size=60)

    def batch_process_orbit(orbit: int) -> None:
        print(orbit)
        try:
            file = open_latest_file(orbit, version, data_file_save_location)
        except FileExistsError:
            return
        add_orbit_attribute_to_file(file, orbit)
        add_version_attribute_to_file(file, version)

        for segment in ['apoapse']:
            file.create_group(f'{segment}')

            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    hduls = get_apoapse_muv_fits_files(iuvs_fits_file_location, orbit)  # TODO: filter out outbound data files labeled apoapse...

                    #file.create_group('apoapse/apsis')
                    #apoapse.apsis.add_apsis_data_to_file(file, approximate_apoapsis_ephemeris_times)

                    apoapse_integration_path = 'apoapse/integration'
                    file.create_group(apoapse_integration_path)
                    integration.add_ephemeris_time_to_file(file, apoapse_integration_path, hduls)
                    integration.add_mirror_data_number_to_file(file, apoapse_integration_path, hduls)
                    integration.add_field_of_view_to_file(file, apoapse_integration_path, hduls)
                    integration.add_case_temperature_to_file(file, apoapse_integration_path, hduls)
                    integration.add_integration_time_to_file(file, apoapse_integration_path, hduls)
                    integration.add_data_file_to_file(file, apoapse_integration_path, hduls)
                    integration.add_apoapse_swath_number_to_file(file, apoapse_integration_path, orbit)
                    integration.add_apoapse_number_of_swaths_to_file(file, apoapse_integration_path, orbit)
                    integration.add_opportunity_classification_to_file(file, apoapse_integration_path)

                    apoapse_spacecraft_geometry_path = 'apoapse/spacecraft_geometry'
                    file.create_group(apoapse_integration_path)
                    spacecraft_geometry.add_subsolar_latitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subsolar_longitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_latitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_longitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_altitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_spacecraft_velocity_inertial_frame_to_file(file, apoapse_spacecraft_geometry_path, hduls)

                    apoapse_instrument_geometry_path = 'apoapse/instrument_geometry'
                    file.create_group(apoapse_instrument_geometry_path)
                    instrument_geometry.add_instrument_x_field_of_view_to_file(file, apoapse_instrument_geometry_path, hduls)
                    instrument_geometry.add_instrument_sun_angle_to_file(file, apoapse_instrument_geometry_path, hduls)
                    instrument_geometry.add_app_flip_to_file(file, apoapse_instrument_geometry_path)

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

                                apoapse_muv_integration_path = 'apoapse/muv/integration'
                                file.create_group(apoapse_muv_integration_path)
                                integration.add_detector_temperature_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_mcp_voltage_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_mcp_voltage_gain_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_apoapse_muv_failsafe_integrations_to_file(file, apoapse_muv_integration_path)
                                integration.add_apoapse_muv_dayside_integrations_to_file(file, apoapse_muv_integration_path)
                                integration.add_apoapse_muv_nightside_integrations_to_file(file, apoapse_muv_integration_path)

                                '''
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
