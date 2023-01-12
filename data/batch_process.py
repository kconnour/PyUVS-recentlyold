from pathlib import Path

from iuvs_data_files import DataFinder
from structure import DataFile

from _integration import Integration



if __name__ == '__main__':
    data_location = Path('/media/kyle/iuvs/production')
    save_location = Path('/media/kyle/iuvs/apoapse')

    for orbit in [4000]:
        df = DataFile(orbit, save_location)
        df.make_empty_hdf5_groups()

        for segment in ['apoapse']:
            finder = DataFinder(data_location, orbit, segment, 'muv')  # 'muv' cause this stuff is just repeated between muv and fuv so I just need to pick one

            # apsis stuff

            # integration stuff
            integration = Integration(df, finder, f'{segment}/integration')
            integration.add_ephemeris_time()

            # engineering stuff

            for channel in ['muv']:
                finder = DataFinder(data_location, orbit, segment, 'muv')
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

