import h5py
import numpy as np

import pyuvs as pu


path = 'apoapse/pixel_geometry'


def add_pixel_geometry_data_to_file(file: h5py.File) -> None:
    add_lat_lon_to_file(file)


def add_lat_lon_to_file(file: h5py.File):
    def get_data() -> tuple[np.ndarray, np.ndarray]:
        et = file['apoapse/integration/ephemeris_time'][:]
        shape = (et.shape[0], 1024)

        latitude = np.zeros(shape)
        longitude = np.zeros(shape)

        for observation in ['dayside', 'failsafe', 'nightside']:
            bin_vector = file[f'apoapse/muv/{observation}/bin_geometry/bin_vector'][:]
            good_integrations = file[f'apoapse/muv/integration/{observation}'][:]
            spatial_bin_edges = file[f'apoapse/muv/{observation}/binning/spatial_bin_edges'][:]
            if bin_vector.size == 0:
                continue
            lat, lon = pu.pixel_geometry.make_along_slit_lat_lon(bin_vector, spatial_bin_edges, et[good_integrations])
            latitude[good_integrations] = lat
            longitude[good_integrations] = lon
        return latitude, longitude

    dataset = file[path].create_dataset('latitude', data=get_data()[0], compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.latitude

    dataset = file[path].create_dataset('longitude', data=get_data()[1], compression=pu.hdf5_options.compression, compression_opts=pu.hdf5_options.compression_opts)
    dataset.attrs['unit'] = pu.units.longitude
