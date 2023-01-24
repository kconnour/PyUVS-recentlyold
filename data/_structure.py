from pathlib import Path

import h5py

from _miscellaneous import Orbit


def make_hdf5_filename(orbit: int, save_location: Path) -> Path:
    orbit = Orbit(orbit)
    filename = f'{orbit.code}.hdf5'
    return save_location / orbit.block / filename


def open_latest_file(filepath: Path) -> h5py.File:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        f = h5py.File(filepath, mode='x')  # 'x' means to create the file but fail if it already exists
    except FileExistsError:
        f = h5py.File(filepath, mode='r+')  # 'r+' means read/write and file must exist
    return f


def make_empty_hdf5_groups(file: h5py.File) -> None:
    # require_group will make it if it doesn't exist. Useful for adding groups in later version
    for segment in ['apoapse']:
        segment_group = file.require_group(segment)

        match segment:
            case 'apoapse':
                apsis = segment_group.require_group('apsis')

                apsis.require_dataset('ephemeris_time', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('mars_year', shape=(1,), dtype='i2', exact=True)
                apsis.require_dataset('solar_longitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('sol', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subsolar_latitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subsolar_longitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subspacecraft_latitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subspacecraft_longitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subspacecraft_altitude', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subspacecraft_local_time', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('mars_sun_distance', shape=(1,), dtype='f8', exact=True)
                apsis.require_dataset('subsolar_subspacecraft_angle', shape=(1,), dtype='f8', exact=True)

            case 'periapse':
                segment_group.require_group('apsis')

        segment_group.require_group('integration')
        segment_group.require_group('pixel_geometry')
        segment_group.require_group('spacecraft_geometry')

        for channel in ['muv']:
            channel_group = segment_group.require_group(channel)
            channel_group.require_group('integration')

            # NOTE: in theory, we can do an experiment in MUV but take FUV data nominally, and vice versa. So the experiments
            #  should be under the channels
            for experiment in ['science', 'relay', 'failsafe']:
                experiment_group = channel_group.require_group(experiment)

                match experiment:
                    case 'science':
                        for daynight in ['dayside', 'nightside']:
                            daynight_group = experiment_group.require_group(daynight)
                            daynight_group.require_group('binning')
                            daynight_group.require_group('detector')
                            daynight_group.require_group('bin_geometry')
                            match daynight:
                                case 'dayside':
                                    daynight_group.require_group('retrievals')
                                case 'nightside':
                                    daynight_group.require_group('mlr')
                    case 'relay':
                        experiment_group.require_group('binning')
                        experiment_group.require_group('detector')
                        experiment_group.require_group('bin_geometry')
                    case 'failsafe':
                        experiment_group.require_group('binning')
                        experiment_group.require_group('detector')
                        experiment_group.require_group('bin_geometry')
