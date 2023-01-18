from datetime import datetime
from pathlib import Path

from astropy.io import fits

from _miscellaneous import Orbit, determine_dayside_files
import _apsis as apsis
import _binning as binning
import _detector as detector
import _integration as integration
import _pixel_geometry as pixel_geometry
import _spacecraft_geometry as spacecraft_geometry
import _spice as spice
import _structure as structure


if __name__ == '__main__':
    # Define paths
    data_location = Path('/media/kyle/iuvs/production')
    spice_location = Path('/media/kyle/iuvs/spice')
    save_location = Path('/media/kyle/iuvs/data')

    # Get the ephemeris times of apsis
    spice.clear_existing_kernels()
    spice.furnish_standard_kernels(spice_location)
    # TODO: See if I can compute the latest datetime of the kernels I have and use that
    # TODO: Change 1 minute resolution to 1 second since I only have to compute it once I can tank the time penalty
    apoapsis_orbits, apoapsis_ephemeris_times = spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2019, 1, 1), step_size=60)

    for orbit in range(3400, 3405):
        print(orbit)
        hdf5_filename = structure.make_hdf5_filename(orbit, save_location)
        file = structure.open_latest_file(hdf5_filename)
        structure.make_empty_hdf5_groups(file)
        file.attrs['orbit'] = orbit

        for segment in ['apoapse']:
            # Get some data to work with. For FUV/MUV independent data, just choose whatever channel
            data_files = sorted((data_location / Orbit(orbit).block).glob(f'*{segment}*{Orbit(orbit).code}*muv*.gz'))
            hduls = [fits.open(f) for f in data_files]
            segment_path = f'{segment}'

            # Add apsis
            if segment in ['apoapse']:  # can be expanded to periapse here
                match segment:
                    case 'apoapse':
                        apsis_ephemeris_times = apoapsis_ephemeris_times
                apsis_path = f'{segment}/apsis'
                apsis.add_apsis_ephemeris_time(file, apsis_path, apsis_ephemeris_times)
                apsis.add_mars_year(file, apsis_path)
                apsis.add_solar_longitude(file, apsis_path)
                apsis.add_sol(file, apsis_path)
                apsis.add_subsolar_latitude(file, apsis_path)
                apsis.add_subsolar_longitude(file, apsis_path)
                apsis.add_subspacecraft_latitude(file, apsis_path)
                apsis.add_subspacecraft_longitude(file, apsis_path)
                apsis.add_subspacecraft_altitude(file, apsis_path)
                apsis.add_mars_sun_distance(file, apsis_path)
                apsis.add_subsolar_subspacecraft_angle(file, apsis_path)

            # Add integration data
            integration_path = f'{segment}/integration'
            integration.add_ephemeris_time(file, integration_path, hduls)
            integration.add_field_of_view(file, integration_path, hduls)
            integration.add_mirror_data_number(file, integration_path, hduls)
            integration.add_detector_temperature(file, integration_path, hduls)
            integration.add_case_temperature(file, integration_path, hduls)
            integration.add_integration_time(file, integration_path, hduls)
            integration.add_swath_number(file, integration_path)
            integration.add_relay_classification(file, integration_path)

            # Add spacecraft geometry data
            spacecraft_geometry_path = f'{segment}/spacecraft_geometry'
            spacecraft_geometry.add_subsolar_latitude(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_subsolar_longitude(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_subspacecraft_latitude(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_subspacecraft_longitude(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_subspacecraft_altitude(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_instrument_sun_angle(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_spacecraft_velocity_inertial_frame(file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_instrument_x_field_of_view(file, spacecraft_geometry_path, hduls)

            # Add APP flip data
            spacecraft_geometry.add_app_flip(file, spacecraft_geometry_path, segment_path)

            for channel in ['muv']:
                data_files = sorted((data_location / Orbit(orbit).block).glob(f'*{segment}*{Orbit(orbit).code}*{channel}*.gz'))
                hduls = [fits.open(f) for f in data_files]

                # Add MUV integration data
                integration_channel_path = f'{segment}/{channel}/integration'
                integration.add_voltage(file, integration_channel_path, hduls)
                integration.add_voltage_gain(file, integration_channel_path, hduls)
                if segment == 'apoapse' and channel == 'muv':
                    integration.add_dayside_integrations(file, integration_channel_path)

                dayside_files = determine_dayside_files(hduls)

                for daynight in [True, False]:
                    dn = 'dayside' if daynight else 'nightside'
                    daynight_hduls = [f for c, f in enumerate(hduls) if dayside_files[c]==daynight]

                    # Add binning data
                    binning_path = f'{segment}/{channel}/{dn}/binning'
                    binning.add_spatial_bin_edges(file, binning_path, daynight_hduls)
                    binning.add_spectral_bin_edges(file, binning_path, daynight_hduls)

                    # Add detector data
                    detector_path = f'{segment}/{channel}/{dn}/detector'
                    detector.add_raw(file, detector_path, daynight_hduls, segment_path)
                    detector.add_dark_subtracted(file, detector_path, daynight_hduls, segment_path)
                    detector.add_brightness(file, detector_path, daynight_hduls, segment_path, binning_path, integration_path, integration_channel_path, daynight)

                    # Add pixel geometry data
                    pixel_geometry_path = f'{segment}/{channel}/{dn}/pixel_geometry'
                    pixel_geometry.add_latitude(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_longitude(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_tangent_altitude(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_tangent_altitude_rate(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_line_of_sight(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_solar_zenith_angle(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_emission_angle(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_phase_angle(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_zenith_angle(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_local_time(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_right_ascension(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_declination(file, pixel_geometry_path, daynight_hduls, segment_path)
                    pixel_geometry.add_pixel_vector(file, pixel_geometry_path, daynight_hduls, segment_path)

                    if daynight:
                        # retrieval stuff
                        pass
                    else:
                        # mlr stuff
                        pass
