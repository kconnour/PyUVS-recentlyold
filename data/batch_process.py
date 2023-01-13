from pathlib import Path

from astropy.io import fits

from _structure import DataFile
from _miscellaneous import Orbit, determine_dayside_files
import _binning as binning
import _detector as detector
import _integration as integration
import _pixel_geometry as pixel_geometry
import _spacecraft_geometry as spacecraft_geometry


if __name__ == '__main__':
    data_location = Path('/media/kyle/iuvs/production')
    save_location = Path('/media/kyle/iuvs/apoapse')

    for orbit in [4000]:
        data_file = DataFile(orbit, save_location)
        data_file.make_empty_hdf5_groups()
        data_file.file.attrs['orbit'] = orbit

        for segment in ['apoapse']:
            data_files = sorted((data_location / Orbit(orbit).block).glob(f'*{segment}*{Orbit(orbit).code}*muv*.gz'))
            hduls = [fits.open(f) for f in data_files]

            # apsis stuff

            # integration stuff
            integration_path = f'{segment}/integration'
            integration.add_ephemeris_time(data_file, integration_path, hduls)
            integration.add_field_of_view(data_file, integration_path, hduls)
            integration.add_mirror_data_number(data_file, integration_path, hduls)
            integration.add_detector_temperature(data_file, integration_path, hduls)
            integration.add_case_temperature(data_file, integration_path, hduls)
            integration.add_integration_time(data_file, integration_path, hduls)
            integration.add_swath_number(data_file, integration_path)
            integration.add_relay_classification(data_file, integration_path)

            # spacecraft_geometry stuff
            spacecraft_geometry_path = f'{segment}/spacecraft_geometry'
            spacecraft_geometry.add_sub_spacecraft_latitude(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_sub_spacecraft_longitude(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_sub_solar_latitude(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_sub_solar_longitude(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_spacecraft_altitude(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_instrument_sun_angle(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_spacecraft_velocity_inertial_frame(data_file, spacecraft_geometry_path, hduls)
            spacecraft_geometry.add_instrument_x_field_of_view(data_file, spacecraft_geometry_path, hduls)

            # Add APP flip
            spacecraft_geometry.add_app_flip(data_file, spacecraft_geometry_path)

            for channel in ['muv']:
                data_files = sorted((data_location / Orbit(orbit).block).glob(f'*{segment}*{Orbit(orbit).code}*{channel}*.gz'))
                hduls = [fits.open(f) for f in data_files]

                # muv integration stuff
                integration_channel_path = f'{segment}/{channel}/integration'
                integration.add_voltage(data_file, integration_channel_path, hduls)
                integration.add_voltage_gain(data_file, integration_channel_path, hduls)
                if segment == 'apoapse' and channel == 'muv':
                    integration.add_dayside_integrations(data_file, integration_channel_path)

                dayside_files = determine_dayside_files(hduls)

                for daynight in [True, False]:
                    dn = 'dayside' if daynight else 'nightside'
                    daynight_hduls = [f for c, f in enumerate(hduls) if dayside_files[c]==daynight]

                    # binning stuff
                    binning_path = f'{segment}/{channel}/{dn}/binning'
                    binning.add_spatial_bin_edges(data_file, binning_path, daynight_hduls)
                    binning.add_spectral_bin_edges(data_file, binning_path, daynight_hduls)

                    # detector stuff
                    detector_path = f'{segment}/{channel}/{dn}/detector'
                    detector.add_raw(data_file, detector_path, daynight_hduls)
                    detector.add_dark_subtracted(data_file, detector_path, daynight_hduls)
                    detector.add_brightness(data_file, detector_path, binning_path, integration_path, integration_channel_path, daynight)

                    # pixel_geometry stuff
                    pixel_geometry_path = f'{segment}/{channel}/{dn}/pixel_geometry'
                    pixel_geometry.add_latitude(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_longitude(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_tangent_altitude(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_solar_zenith_angle(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_emission_angle(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_phase_angle(data_file, pixel_geometry_path, daynight_hduls)
                    pixel_geometry.add_local_time(data_file, pixel_geometry_path, daynight_hduls)

                    if daynight:
                        # retrieval stuff
                        pass
                    else:
                        # mlr stuff
                        pass
