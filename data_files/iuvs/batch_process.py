from pathlib import Path
from datetime import datetime
import multiprocessing as mp

import file_datasets
import file_setup
import fits_sort
import apsis
import apsis_additions
import spice

# Note: I absolutely cannot think of a way to version each array in a smart way. The code just gets out of control
# when thinking that I have to track all the dependencies of a change in the code. Assigning a singular version to the
# entire file is the only sensible solution I can think of


p = Path('/media/kyle/iuvs/production/orbit03000')
files = sorted(p.glob('*apoapse*orbit03000*muv*.gz'))

'''from astropy.io import fits
for foo in files:
    hdul = fits.open(foo)
    print(hdul['pixelgeometry'].data['pixel_solar_zenith_angle'].shape)

raise SystemExit(9)'''

if __name__ == '__main__':
    version: int = 1

    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    spice.clear_existing_kernels()
    spice.furnish_standard_kernels(spice_kernel_location)
    apoapsis_orbits, approximate_apoapsis_ephemeris_times = spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2022, 9, 2), step_size=60)

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
                    apsis_additions.add_apsis_data_to_file(file, approximate_apoapsis_ephemeris_times)

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
                    file_datasets.add_subsolar_latitude_to_file(file, spacecraft_geometry_path, segment_hduls)
                    file_datasets.add_subsolar_longitude_to_file(file, spacecraft_geometry_path, segment_hduls)
                    file_datasets.add_subspacecraft_latitude_to_file(file, spacecraft_geometry_path, segment_hduls)
                    file_datasets.add_subspacecraft_longitude_to_file(file, spacecraft_geometry_path, segment_hduls)
                    file_datasets.add_subspacecraft_altitude_to_file(file, spacecraft_geometry_path, segment_hduls)
                    file_datasets.add_spacecraft_velocity_inertial_frame_to_file(file, spacecraft_geometry_path, segment_hduls)

                    instrument_geometry_path = f'{segment_path}/instrument_geometry'
                    file.create_group(instrument_geometry_path)
                    file_datasets.add_instrument_x_field_of_view_to_file(file, instrument_geometry_path, segment_hduls)
                    file_datasets.add_instrument_sun_angle_to_file(file, instrument_geometry_path, segment_hduls)
                    file_datasets.add_app_flip_to_file(file, instrument_geometry_path, spacecraft_geometry_path)

                    for channel in ['muv']:
                        channel_path = f'{segment}/{channel}'
                        file.create_group(channel_path)

                        match channel:
                            case 'muv':
                                # Get the data files for this channel
                                apoapse_muv_hduls = fits_sort.get_apoapse_muv_fits_files(iuvs_fits_file_location, orbit)

                                channel_integration_path = f'{channel_path}/integration'
                                file.create_group(channel_integration_path)
                                file_datasets.add_detector_temperature_to_file(file, channel_integration_path, apoapse_muv_hduls)
                                file_datasets.add_mcp_voltage_to_file(file, channel_integration_path, apoapse_muv_hduls)
                                file_datasets.add_mcp_voltage_gain_to_file(file, channel_integration_path, apoapse_muv_hduls)
                                file_datasets.add_apoapse_muv_failsafe_integrations_to_file(file, channel_integration_path)
                                file_datasets.add_apoapse_muv_dayside_integrations_to_file(file, channel_integration_path)
                                file_datasets.add_apoapse_muv_nightside_integrations_to_file(file, channel_integration_path)

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
                                    file_datasets.add_spatial_bin_edges(file, binning_path, experiment_hduls)
                                    file_datasets.add_spectral_bin_edges(file, binning_path, experiment_hduls)

                                    spatial_bin_geometry_path = f'{experiment_path}/spatial_bin_geometry'
                                    file.create_group(spatial_bin_geometry_path)
                                    file_datasets.add_latitude(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_longitude(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_tangent_altitude(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_tangent_altitude_rate(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_line_of_sight(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_solar_zenith_angle(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_emission_angle(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_phase_angle(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_zenith_angle(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_local_time(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_right_ascension(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_declination(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_bin_vector(file, spatial_bin_geometry_path, instrument_geometry_path, experiment_hduls)

                                    detector_path = f'{experiment_path}/detector'
                                    file.create_group(detector_path)
                                    file_datasets.add_raw(file, detector_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_dark_subtracted(file, detector_path, instrument_geometry_path, experiment_hduls)
                                    file_datasets.add_brightness(file, detector_path, instrument_geometry_path, binning_path, integration_path, channel_integration_path, experiment)

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
                    # TODO: pixel geometry
        file.close()

    for orb in range(3203, 4000):
        batch_process_orbit(orb)

    #n_cpus = mp.cpu_count()
    #pool = mp.Pool(n_cpus -1)

    #for orb in range(3000, 3100):
        #pool.apply_async(func=batch_process_orbit, args=(orb,))
    #pool.close()
    #pool.join()
