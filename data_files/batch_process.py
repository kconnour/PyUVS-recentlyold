import math
from pathlib import Path

from astropy.io import fits
import h5py

from _spacecraft_geometry import add_spacecraft_geometry_data_to_file


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


if __name__ == '__main__':
    # Define paths
    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    for orbit in range(1, 100):
        print(orbit)
        orbit_block = make_orbit_block(orbit)
        orbit_code = make_orbit_code(orbit)
        hdf5_filename = make_hdf5_filename(orbit, data_file_save_location)
        file = open_latest_file(hdf5_filename)
        file.attrs['orbit'] = orbit

        for segment in ['apoapse']:
            segment_path = f'{segment}'
            file.require_group(segment_path)

            # Add apsis
            match segment:
                case 'apoapse' | 'periapse':
                    apsis_path = f'{segment}/apsis'
                    file.require_group(apsis_path)
                    # TODO: add ephemeris time
                    # TODO: add mars year
                    # TODO: add Ls
                    # TODO: add sol
                    # TODO: add subsolar latitude
                    # TODO: add subsolar longitude
                    # TODO: add subspacecraft latitude
                    # TODO: add subspacecraft longitude
                    # TODO: add subspacecraft altitude
                    # TODO: add subspacecraft local time
                    # TODO: add mars sun distance
                    # TODO: add subsolar subspacecraft angle

            # Get some data to work with. For FUV/MUV independent data, just choose whatever channel
            data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*muv*.gz'))
            hduls = [fits.open(f) for f in data_files]

            # Add MUV/FUV-independent integration data
            integration_path = f'{segment}/integration'
            file.require_group(integration_path)
            # TODO: add timestamp
            # TODO: add ephemeris time
            # TODO: add mirror DN
            # TODO: add field of view
            # TODO: add case temperature
            # TODO: add integration time
            # TODO: add swath number
            # TODO: add relay classification

            # Add spacecraft geometry data
            spacecraft_geometry_path = f'{segment}/spacecraft_geometry'
            file.require_group(spacecraft_geometry_path)
            add_spacecraft_geometry_data_to_file(file, spacecraft_geometry_path, hduls)

            # Add pixel geometry
            pixel_geometry_path = f'{segment}/pixel_geometry'
            file.require_group(pixel_geometry_path)
            # TODO: add pixel geometry data

            for channel in ['muv']:
                # Get the data files for this channel
                data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*{channel}*.gz'))
                hduls = [fits.open(f) for f in data_files]

                # Add this channel's specific integration data
                integration_channel_path = f'{segment}/{channel}/integration'

                file.require_group(integration_channel_path)
                # TODO: add detector temperature
                # TODO: add voltage
                # TODO: add voltage gain

                for collection in ['opportunity', 'science']:
                    match collection:
                        case 'opportunity':
                            # Get the relay data files
                            relay_path = f'{segment}/{channel}/{collection}'

                            # Add binning data
                            binning_path = f'{relay_path}/binning'
                            file.require_group(binning_path)
                            # TODO: binning

                            # Add detector data
                            detector_path = f'{relay_path}/detector'
                            file.require_group(detector_path)
                            # TODO: detector

                            # Add bin geometry data
                            bin_geometry_path = f'{relay_path}/bin_geometry'
                            file.require_group(bin_geometry_path)
                            # TODO: bin geometry

                        case 'science':
                            # TODO: get science hduls
                            for experiment in ['failsafe', 'nominal']:
                                match experiment:
                                    case 'failsafe':
                                        failsafe_path = f'{segment}/{channel}/{collection}/{experiment}'

                                        # Add binning data
                                        binning_path = f'{failsafe_path}/binning'
                                        file.require_group(binning_path)
                                        # TODO: binning

                                        # Add detector data
                                        detector_path = f'{failsafe_path}/detector'
                                        file.require_group(detector_path)
                                        # TODO: detector

                                        # Add bin geometry data
                                        bin_geometry_path = f'{failsafe_path}/bin_geometry'
                                        file.require_group(bin_geometry_path)
                                        # TODO: bin geometry

                                    case 'nominal':
                                        # TODO: get nominal hduls
                                        for daynight in ['dayside', 'nightside']:
                                            # TODO: get daynight hduls
                                            daynight_path = f'{segment}/{channel}/{collection}/{experiment}/{daynight}'

                                            # Add binning data
                                            binning_path = f'{daynight_path}/binning'
                                            file.require_group(binning_path)
                                            # TODO: binning

                                            # Add detector data
                                            detector_path = f'{daynight_path}/detector'
                                            file.require_group(detector_path)
                                            # TODO: detector

                                            # Add bin geometry data
                                            bin_geometry_path = f'{daynight_path}/bin_geometry'
                                            file.require_group(bin_geometry_path)
                                            # TODO: bin geometry

                                            match daynight:
                                                case 'dayside':
                                                    pass
                                                case 'nightside':
                                                    pass
