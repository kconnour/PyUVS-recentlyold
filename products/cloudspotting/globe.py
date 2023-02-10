import multiprocessing as mp
from pathlib import Path

import cartopy.crs as ccrs
import h5py
import matplotlib.pyplot as plt
import numpy as np

import pyuvs as pu


def checkerboard():
    """
    Create an 5-degree-size RGB checkerboard array for display with matplotlib.pyplot.imshow().

    Parameters
    ----------
    None.

    Returns
    -------
    grid : array
        The checkerboard grid.
    """

    # make and transpose the grid (don't ask how it's done)
    grid = np.repeat(np.kron([[0.67, 0.33] * 36, [0.33, 0.67] * 36] * 18, np.ones((5, 5)))[:, :, None], 3, axis=2)

    # return the array
    return grid


def latlon_meshgrid(latitude, longitude, altitude):
    # make meshgrids to hold latitude and longitude grids for pcolormesh display
    X = np.zeros((latitude.shape[0] + 1, latitude.shape[1] + 1))
    Y = np.zeros((longitude.shape[0] + 1, longitude.shape[1] + 1))
    mask = np.ones((latitude.shape[0], latitude.shape[1]))

    # loop through pixel geometry arrays
    for i in range(int(latitude.shape[0])):
        for j in range(int(latitude.shape[1])):

            # there are some pixels where some of the pixel corner longitudes are undefined
            # if we encounter one of those, set the data value to missing so it isn't displayed
            # with pcolormesh
            if np.size(np.where(np.isfinite(longitude[i, j]))) != 5:
                mask[i, j] = np.nan

            # also mask out non-disk pixels
            if altitude[i, j] != 0:
                mask[i, j] = np.nan

            # place the longitude and latitude values in the meshgrids
            X[i, j] = longitude[i, j, 1]
            X[i + 1, j] = longitude[i, j, 0]
            X[i, j + 1] = longitude[i, j, 3]
            X[i + 1, j + 1] = longitude[i, j, 2]
            Y[i, j] = latitude[i, j, 1]
            Y[i + 1, j] = latitude[i, j, 0]
            Y[i, j + 1] = latitude[i, j, 3]
            Y[i + 1, j + 1] = latitude[i, j, 2]

    # set any of the NaN values to zero (otherwise pcolormesh will break even if it isn't displaying the pixel).
    X[np.where(~np.isfinite(X))] = 0
    Y[np.where(~np.isfinite(Y))] = 0

    # set to domain [-180,180)
    X[np.where(X > 180)] -= 360

    # return the coordinate arrays and the mask
    return X, Y


def make_apoapse_muv_globe(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = h5py.File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    brightness = f['apoapse/muv/dayside/detector/brightness'][:]

    if brightness.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:]
    tangent_altitude = f['apoapse/muv/dayside/bin_geometry/tangent_altitude'][:][..., 4]
    solar_zenith_angle = f['apoapse/muv/dayside/bin_geometry/solar_zenith_angle'][:]
    latitude = f['apoapse/muv/dayside/bin_geometry/latitude'][:]
    longitude = f['apoapse/muv/dayside/bin_geometry/longitude'][:]
    subspacecraft_latitude = f['apoapse/apsis/subspacecraft_latitude'][:][0]
    subspacecraft_longitude = f['apoapse/apsis/subspacecraft_longitude'][:][0]
    subspacecraft_altitude = f['apoapse/apsis/subspacecraft_altitude'][:][0]

    solar_zenith_angle[tangent_altitude != 0] = np.nan

    if brightness.size == 0:
        return

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    try:
        rgb_image = pu.colorize.histogram_equalize_detector_image(brightness, mask=mask) / 255
    except IndexError:
        return

    # Setup the graphic
    rmars = 3400
    fig = plt.figure(figsize=(6, 6), facecolor='w')
    globe = ccrs.Globe(semimajor_axis=rmars * 1e3, semiminor_axis=rmars * 1e3)
    projection = ccrs.NearsidePerspective(central_latitude=subspacecraft_latitude, central_longitude=subspacecraft_longitude,
                                          satellite_height=subspacecraft_altitude * 10 ** 3, globe=globe)
    transform = ccrs.PlateCarree(globe=globe)
    globe_ax = plt.axes(projection=projection)

    checkerboard_surface = checkerboard() * 0.1
    globe_ax.imshow(checkerboard_surface, transform=transform, extent=[-180, 180, -90, 90])

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath

        x, y = latlon_meshgrid(latitude[swath_indices], longitude[swath_indices], tangent_altitude[swath_indices])

        rgb = rgb_image[swath_indices]
        fill = rgb[..., 0]

        colors = np.reshape(rgb, (rgb.shape[0] * rgb.shape[1], rgb.shape[2]))
        globe_ax.pcolormesh(x, y, fill, color=colors, linewidth=0, edgecolors='none', rasterized=True,
                            transform=transform).set_array(None)

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_binning = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_binning = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = f'{orbit_code}-Ls{solar_longitude * 10:04.0f}-angle{subsolar_subspacecraft_angle * 10:04.0f}-binning{spatial_binning:04}x{spectral_binning:04}-heq-globe.png'

    plt.savefig(save_location / filename)
    plt.close(fig)


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/home/kyle/iuvs/cloudspotting/')

    n_cpus = mp.cpu_count()
    pool = mp.Pool(n_cpus -1)

    for orb in range(1, 1000):
        pool.apply_async(func=make_apoapse_muv_globe, args=(orb,))

    pool.close()
    pool.join()
