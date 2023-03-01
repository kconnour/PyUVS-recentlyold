from h5py import File
import numpy as np

gb = [File('/media/kyle/iuvs/data/orbit03200/orbit03255_v01.hdf5'), File('/media/kyle/iuvs/data/orbit03200/orbit03256_v01.hdf5')]

for f in gb:
    x = f['apoapse/instrument_geometry/instrument_x_field_of_view'][:]
    v = f['apoapse/spacecraft_geometry/spacecraft_velocity_inertial_frame'][:]

    foo = x[:, 0] * v[:, 0]
    print(np.sum(foo))
