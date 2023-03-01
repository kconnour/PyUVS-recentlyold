from astropy.io import fits
from h5py import File
import numpy as np


version: int = 1

'''og_ice = fits.open('/home/kyle/Downloads/dust_all.fits(1).gz')
og_ice.info()

print(og_ice['forw'].data.shape)
print(og_ice['scattering_angle'].data)
#raise SystemExit(9)

ice = File(f'/home/kyle/iuvs/mars_dust_v{version:02}.hdf5', mode='x')

ice.attrs['comment'] = 'The data in this file was created by Mike Wolff using the database of Saito et al., 2021, Atmos. Sci., 78, 2089???2111'
ice.attrs['sphericity'] = 0.78
ds = ice.create_dataset('particle_sizes', data=og_ice['particle_sizes'].data)
ds.attrs['unit'] = 'Microns'

ds = ice.create_dataset('wavelengths', data=og_ice['wavelengths'].data)
ds.attrs['unit'] = 'Microns'

ds = ice.create_dataset('scattering_angle', data=og_ice['scattering_angle'].data)
ds.attrs['unit'] = 'Degrees'

ds = ice.create_dataset('scattering_cross_section', data=og_ice['forw'].data[..., 1])
ds = ice.create_dataset('extinction_cross_section', data=og_ice['forw'].data[..., 0])
ds = ice.create_dataset('asymmetry_parameter', data=og_ice['forw'].data[..., 2])

ds = ice.create_dataset('legendre_coefficients', data=np.moveaxis(og_ice['pmom'].data, 0, -1))
ds = ice.create_dataset('phase_function', data=np.moveaxis(og_ice['expansion'].data, 0, -1))

ice.close()

raise SystemExit(9)'''



og_ice = fits.open('/home/kyle/Downloads/droxtal_050_tmat1_reff_v010.fits')
og_ice.info()
print(og_ice['primary'].header)

print(og_ice['forw'].data.shape)
#raise SystemExit(9)
print(og_ice['pmom'].data.shape)

ice = File(f'/home/kyle/iuvs/mars_water-ice_v{version:02}.hdf5', mode='x')

ice.attrs['comment'] = 'The data in this file was created by Mike Wolff using T-matrix calculations of droxtals taken from: Yang et al.,J. Atm Science (2013): 330-347 and Bi, Lei, and Ping Yang, JQSRT 189 (2017): 228-237'
ice.attrs['size_distribution'] = 0.3
ds = ice.create_dataset('particle_sizes', data=og_ice['particle_sizes'].data)
ds.attrs['unit'] = 'Microns'

ds = ice.create_dataset('wavelengths', data=og_ice['wavelengths'].data)
ds.attrs['unit'] = 'Microns'

ds = ice.create_dataset('scattering_angle', data=og_ice['scattering_angle'].data)
ds.attrs['unit'] = 'Degrees'

ds = ice.create_dataset('scattering_cross_section', data=og_ice['forw'].data[..., 1])
ds = ice.create_dataset('extinction_cross_section', data=og_ice['forw'].data[..., 0])
ds = ice.create_dataset('asymmetry_parameter', data=og_ice['forw'].data[..., 2])

ds = ice.create_dataset('legendre_coefficients', data=np.moveaxis(og_ice['pmom'].data, 0, -1))
ds = ice.create_dataset('phase_function', data=np.moveaxis(og_ice['expansion'].data, 0, -1))

ice.close()
