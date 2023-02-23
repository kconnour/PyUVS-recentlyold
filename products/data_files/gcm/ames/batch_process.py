from h5py import File
from netCDF4 import Dataset

import arrays
from hdf5_options import compression, compression_opts


if __name__ == '__main__':
    # TODO: modify these filenames each time
    gcm = Dataset('/home/kyle/iuvs/ames/03704.atmos_diurn.nc')
    file = File('/home/kyle/iuvs/ames/simulation2.hdf5', mode='a')

    # TODO: modify these if necessary
    dust_radprop = File('/home/kyle/iuvs/mars_dust_v01.hdf5')
    ice_radprop = File('/home/kyle/iuvs/mars_water-ice_v01.hdf5')

    dust_target_wavelength = 0.25
    ice_target_wavelength = 0.25

    # Make the arrays that define the model grid
    model_grid = file.create_group('grid')
    ds = model_grid.create_dataset('latitude_centers', data=arrays.make_latitude_centers(gcm))
    ds.attrs['unit'] = 'Degrees [N]'
    ds = model_grid.create_dataset('latitude_edges', data=arrays.make_latitude_edges(gcm))
    ds.attrs['unit'] = 'Degrees [N]'
    ds = model_grid.create_dataset('longitude_centers', data=arrays.make_longitude_centers(gcm))
    ds.attrs['unit'] = 'Degrees [E]'
    ds = model_grid.create_dataset('longitude_edges', data=arrays.make_longitude_edges(gcm))
    ds.attrs['unit'] = 'Degrees [E]'
    ds = model_grid.create_dataset('simulation_sol_centers', data=arrays.make_simulation_sol_centers(gcm))
    ds.attrs['unit'] = 'Total sol number'
    ds = model_grid.create_dataset('simulation_sol_edges', data=arrays.make_simulation_sol_edges(gcm))
    ds.attrs['unit'] = 'Total sol number'
    ds = model_grid.create_dataset('yearly_sol_centers', data=arrays.make_yearly_sol_centers(gcm))
    ds.attrs['unit'] = 'Yearly sol number'
    ds = model_grid.create_dataset('yearly_sol_edges', data=arrays.make_yearly_sol_edges(gcm))
    ds.attrs['unit'] = 'Yearly sol number'
    ds = model_grid.create_dataset('local_time_centers', data=arrays.make_local_time_centers(gcm))
    ds.attrs['unit'] = 'Local time at longitude = 0'
    ds = model_grid.create_dataset('local_time_edges', data=arrays.make_local_time_edges(gcm))
    ds.attrs['unit'] = 'Local time at longitude = 0'
    ds = model_grid.create_dataset('solar_longitude_centers', data=arrays.make_solar_longitude_centers(gcm))
    ds.attrs['unit'] = 'Degrees'
    ds = model_grid.create_dataset('ak', data=arrays.make_ak(gcm))
    ds.attrs['unit'] = 'Pa'
    ds = model_grid.create_dataset('bk', data=arrays.make_bk(gcm))
    ds.attrs['unit'] = 'Unitless'

    # Make the arrays that define the surface
    surface = file.create_group('surface')
    surface_temperature = surface.create_dataset('temperature', data=arrays.make_surface_temperature(gcm),
                                                 compression=compression, compression_opts=compression_opts)
    surface_temperature.attrs['unit'] = 'K'
    surface_pressure = surface.create_dataset('pressure', data=arrays.make_surface_pressure(gcm),
                                              compression=compression, compression_opts=compression_opts)
    surface_pressure.attrs['unit'] = 'Pa'

    # Make the arrays that define the atmosphere
    atmosphere = file.create_group('atmosphere')
    atmosphere_temperature = atmosphere.create_dataset('temperature', data=arrays.make_atmospheric_temperature(gcm),
                                                       compression=compression, compression_opts=compression_opts)
    atmosphere_temperature.attrs['unit'] = 'K'
    atmosphere_pressure = atmosphere.create_dataset('pressure', data=arrays.make_atmospheric_pressure(gcm),
                                                     compression=compression, compression_opts=compression_opts)
    atmosphere_pressure.attrs['unit'] = 'Pa'
    dust_od = atmosphere.create_dataset('dust_optical_depth', data=arrays.make_dust_optical_depth(gcm, dust_radprop, 0.25),
                                        compression=compression, compression_opts=compression_opts)
    dust_od.attrs['comment'] = f'Total column integrated optical depth at {dust_target_wavelength} microns.'

    ice_od = atmosphere.create_dataset('ice_optical_depth', data=arrays.make_ice_optical_depth(gcm, ice_radprop, 0.25),
                                       compression=compression, compression_opts=compression_opts)
    ice_od.attrs['comment'] = f'Total column integrated optical depth at {ice_target_wavelength} microns.'

    file.close()
