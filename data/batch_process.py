from pathlib import Path

from astropy.io import fits

from _structure import DataFile
from _miscellaneous import Orbit
import _integration as integration
import _spacecraft_geometry as spacecraft_geometry


if __name__ == '__main__':
    data_location = Path('/media/kyle/iuvs/production')
    save_location = Path('/media/kyle/iuvs/apoapse')

    for orbit in [7618, 7622]:
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
                data_files = sorted((data_location / Orbit(orbit).block).glob(f'*{segment}*{Orbit(orbit).code}*muv*.gz'))
                hduls = [fits.open(f) for f in data_files]

                # muv integration stuff
                integration_path = f'{segment}/{channel}/integration'
                integration.add_voltage(data_file, integration_path, hduls)
                integration.add_voltage_gain(data_file, integration_path, hduls)
                if channel == 'muv':
                    integration.add_dayside_integrations(data_file, integration_path)

                for daynight in [True, False]:
                    # binning stuff
                    # detector stuff
                    # pixel_geometry stuff
                    if daynight:
                        # retrieval stuff
                        pass
                    else:
                        # mlr stuff
                        pass
