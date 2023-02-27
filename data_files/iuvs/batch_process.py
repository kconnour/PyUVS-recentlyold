from pathlib import Path

import file_datasets
import file_setup
import fits_sort

# Note: I absolutely cannot think of a way to version each array in a smart way. The code just gets out of control
# when thinking that I have to track all the dependencies of a change in the code. Assigning a singular version to the
# entire file is the only sensible solution I can think of

if __name__ == '__main__':
    version: int = 1

    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    '''pu.spice.clear_existing_kernels()
    pu.spice.furnish_standard_kernels(spice_kernel_location)
    apoapsis_orbits, approximate_apoapsis_ephemeris_times = pu.spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2022, 9, 2), step_size=60)'''

    def batch_process_orbit(orbit: int) -> None:
        print(orbit)
        try:
            file = file_setup.open_latest_file(orbit, version, data_file_save_location)
        except FileExistsError:
            return
        file_setup.add_orbit_attribute_to_file(file, orbit)
        file_setup.add_version_attribute_to_file(file, version)

        for segment in ['apoapse']:
            segment_path = f'{segment}'
            file.create_group(segment_path)

            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    segment_hduls = fits_sort.get_apoapse_muv_fits_files(iuvs_fits_file_location, orbit)

                    apsis_path = f'{segment_path}/apsis'
                    file.create_group(apsis_path)
                    '''apoapse.apsis.add_apsis_data_to_file(file, approximate_apoapsis_ephemeris_times)'''

                    integration_path = f'{segment_path}/integration'
                    file.create_group(integration_path)
                    file_datasets.add_ephemeris_time_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_mirror_data_number_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_mirror_angle_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_field_of_view_to_file(file, integration_path)
                    file_datasets.add_case_temperature_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_integration_time_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_data_file_number_to_file(file, integration_path, segment_hduls)
                    file_datasets.add_apoapse_swath_number_to_file(file, integration_path, orbit)
                    file_datasets.add_apoapse_number_of_swaths_to_file(file, integration_path, orbit)
                    file_datasets.add_apoapse_opportunity_classification_to_file(file, integration_path, orbit)

                    spacecraft_geometry_path = f'{segment_path}/spacecraft_geometry'
                    file.create_group(spacecraft_geometry_path)
                    '''spacecraft_geometry.add_subsolar_latitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subsolar_longitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_latitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_longitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_subspacecraft_altitude_to_file(file, apoapse_spacecraft_geometry_path, hduls)
                    spacecraft_geometry.add_spacecraft_velocity_inertial_frame_to_file(file, apoapse_spacecraft_geometry_path, hduls)'''

                    instrument_geometry_path = f'{segment_path}/instrument_geometry'
                    file.create_group(instrument_geometry_path)
                    '''instrument_geometry.add_instrument_x_field_of_view_to_file(file, apoapse_instrument_geometry_path, hduls)
                    instrument_geometry.add_instrument_sun_angle_to_file(file, apoapse_instrument_geometry_path, hduls)
                    instrument_geometry.add_app_flip_to_file(file, apoapse_instrument_geometry_path)'''

                    for channel in ['muv']:
                        channel_path = f'{segment}/{channel}'
                        file.create_group(channel_path)

                        match channel:
                            case 'muv':
                                # Get the data files for this channel
                                apoapse_muv_hduls = fits_sort.get_apoapse_muv_fits_files(iuvs_fits_file_location, orbit)

                                channel_integration_path = f'{channel_path}/integration'
                                file.create_group(channel_integration_path)
                                '''integration.add_detector_temperature_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_mcp_voltage_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_mcp_voltage_gain_to_file(file, apoapse_muv_integration_path, apoapse_muv_hduls)
                                integration.add_apoapse_muv_failsafe_integrations_to_file(file, apoapse_muv_integration_path)
                                integration.add_apoapse_muv_dayside_integrations_to_file(file, apoapse_muv_integration_path)
                                integration.add_apoapse_muv_nightside_integrations_to_file(file, apoapse_muv_integration_path)'''


                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    experiment_path = f'{segment}/{channel}/{experiment}'
                                    file.create_group(experiment_path)

                                    match experiment:
                                        # Get relevant hduls
                                        case 'failsafe':
                                            experiment_hduls = fits_sort.get_apoapse_muv_failsafe_files(apoapse_muv_hduls)
                                        case 'dayside':
                                            experiment_hduls = fits_sort.get_apoapse_muv_dayside_files(apoapse_muv_hduls)
                                        case 'nightside':
                                            experiment_hduls = fits_sort.get_apoapse_muv_nightside_files(apoapse_muv_hduls)

                                    binning_path = f'{experiment_path}/binning'
                                    file.create_group(binning_path)
                                    '''apoapse.muv.failsafe.binning.add_binning_data_to_file(file, failsafe_hduls)'''

                                    detector_path = f'{experiment_path}/detector'
                                    file.create_group(detector_path)
                                    '''apoapse.muv.failsafe.detector.add_detector_data_to_file(file, failsafe_hduls)'''

                                    spatial_bin_geometry_path = f'{experiment_path}/spatial_bin_geometry'
                                    file.create_group(spatial_bin_geometry_path)
                                    '''apoapse.muv.failsafe.bin_geometry.add_bin_geometry_data_to_file(file, failsafe_hduls)'''

                                    match experiment:
                                        case 'dayside':
                                            # TODO: retrievals
                                            pass
                                        case 'nightside':
                                            # TODO: MLR
                                            pass

                    # In theory, I should be able to do this above with SPICE kernels, but since I need the pixel vector
                    #  I'm doing it here
                    spatial_pixel_geometry_path = f'{segment}/spatial_pixel_geometry'
                    file.create_group(spatial_pixel_geometry_path)
                    '''apoapse.pixel_geometry.add_pixel_geometry_data_to_file(file)'''
        file.close()

    for o in range(4000, 4002):
        batch_process_orbit(o)
