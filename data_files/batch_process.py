import math
from pathlib import Path

from astropy.io import fits
import h5py

from _apsis import add_apsis_data_to_file
from _binning import add_binning_data_to_file
from _integration import add_channel_independent_integration_data_to_file, add_channel_dependent_integration_data_to_file
from _miscellaneous import get_opportunity_file_indices, get_failsafe_file_indices, get_dayside_file_indices
from _pixel_geometry import add_pixel_geometry_data_to_file
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

    for orbit in range(5495, 5496):
        print(orbit)
        orbit_block = make_orbit_block(orbit)
        orbit_code = make_orbit_code(orbit)
        file = create_file(orbit)
        # TODO: if overall data product number is up to date, skip the below to not overwrite it

        for segment in ['apoapse']:
            file.require_group(f'{segment}')  # TODO: this seems out of place since the require_group is tucked into other functions elsewhere

            match segment:
                case 'apoapse' | 'periapse':
                    add_apsis_data_to_file(file, f'{segment}/apsis', None)

            # Get some data to work with. For FUV/MUV independent data, just choose either channel
            data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*muv*.gz'))
            hduls = [fits.open(f) for f in data_files]

            # Add groups of data and their datasets
            add_channel_independent_integration_data_to_file(file, f'{segment}/integration', hduls)
            add_spacecraft_geometry_data_to_file(file, f'{segment}/spacecraft_geometry', f'{segment}', hduls)
            add_pixel_geometry_data_to_file(file, f'{segment}/pixel_geometry')

            for channel in ['muv']:
                # Get the data files for this channel
                channel_data_files = sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*{channel}*.gz'))
                channel_hduls = [fits.open(f) for f in channel_data_files]

                # Add this channel's specific integration data
                add_channel_dependent_integration_data_to_file(file, f'{segment}/{channel}/integration', channel_hduls)

                for collection in ['opportunity', 'science']:
                    match collection:
                        case 'opportunity':
                            # Get the opportunity data files
                            opportunity_file_indices = get_opportunity_file_indices(file, f'{segment}/integration')
                            opportunity_hduls = [f for c, f in enumerate(channel_hduls) if c in opportunity_file_indices]

                            # Add groups of data and their datasets
                            opportunity_path = f'{segment}/{channel}/{collection}'
                            add_binning_data_to_file(file, f'{opportunity_path}/binning', opportunity_hduls)
                            # TODO: detector
                            # TODO: bin geometry

                        case 'science':
                            science_hduls = [f for f in channel_hduls if f not in opportunity_hduls]
                            for experiment in ['failsafe', 'nominal']:
                                match experiment:
                                    case 'failsafe':
                                        # Get the failsafe data files
                                        failsafe_file_indices = get_failsafe_file_indices(file, f'{segment}/integration', f'{segment}/{channel}/integration')
                                        failsafe_hduls = [f for c, f in enumerate(channel_hduls) if c in failsafe_file_indices and f in science_hduls]

                                        # Add groups of data and their datasets
                                        experiment_path = f'{segment}/{channel}/{collection}/{experiment}'
                                        add_binning_data_to_file(file, f'{experiment_path}/binning', failsafe_hduls)
                                        # TODO: detector
                                        # TODO: bin geometry

                                    case 'nominal':
                                        nominal_hduls = [f for f in channel_hduls if f not in failsafe_hduls and f not in opportunity_hduls]
                                        for daynight in ['dayside', 'nightside']:
                                            experiment_path = f'{segment}/{channel}/{collection}/{experiment}/{daynight}'
                                            match daynight:
                                                case 'dayside':
                                                    # Get the dayside data files
                                                    dayside_file_indices = get_dayside_file_indices(file, f'{segment}/integration', f'{segment}/{channel}/integration')
                                                    dayside_hduls = [f for c, f in enumerate(channel_hduls) if c in dayside_file_indices and f in nominal_hduls]

                                                    # Add groups of data and their datasets
                                                    add_binning_data_to_file(file, f'{experiment_path}/binning', dayside_hduls)
                                                    # TODO: detector
                                                    # TODO: bin geometry

                                                case 'nightside':
                                                    nightside_hduls = [f for f in nominal_hduls if f not in dayside_hduls]

                                                    # Add groups of data and their datasets
                                                    add_binning_data_to_file(file, f'{experiment_path}/binning', nightside_hduls)
                                                    # TODO: detector
                                                    # TODO: bin geometry
