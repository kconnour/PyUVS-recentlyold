from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt

files = sorted(Path('/media/kyle/iuvs/production/orbit00200').glob('*apoapse*orbit00240*fuv*.gz'))

fig, ax = plt.subplots(2, 1)

hdul = fits.open(files[0])
pri = hdul['primary'].data[..., -1]
print(hdul['integration'].data['fov_deg'])

'''ax[0].imshow(pri)

hdul = fits.open(files[1])
pri = hdul['primary'].data[..., -1]

ax[1].imshow(pri)


plt.savefig('/home/kyle/junk.png')'''