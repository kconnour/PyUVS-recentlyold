import multiprocessing as mp
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np

from images import graphics
import pyuvs as pu
from _filename import make_filename


def setup_figure(n_swaths: int, angular_width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    field_of_view = (pu.constants.maximum_mirror_angle - pu.constants.minimum_mirror_angle) * 2
    width = n_swaths * angular_width / field_of_view * height
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    return fig, ax


def make_histogram_equalized_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = h5py.File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    brightness = f['apoapse/muv/dayside/detector/brightness'][:]

    if brightness.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:]
    tangent_altitude = f['apoapse/muv/dayside/bin_geometry/tangent_altitude'][:][..., 4]
    field_of_view = f['apoapse/integration/field_of_view'][:]
    solar_zenith_angle = f['apoapse/muv/dayside/bin_geometry/solar_zenith_angle'][:]
    spatial_bin_edges = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:]

    solar_zenith_angle[tangent_altitude != 0] = np.nan

    if brightness.size == 0:
        return

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    image = graphics.histogram_equalize_detector_image(brightness, mask=mask) / 255

    angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width

    fig, ax = setup_figure(swath_number[-1] + 1, angular_width, 6)

    graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width)
    graphics.add_terminator_contour_line_to_axis(ax, solar_zenith_angle, swath_number, field_of_view, angular_width)

    ax.set_xlim(0, angular_width * (swath_number[-1] + 1))
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_bin_width = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_bin_width = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = make_filename(orbit_code, solar_longitude, subsolar_subspacecraft_angle, spatial_bin_width, spectral_bin_width, 'heq', 'ql')
    plt.savefig(save_location / filename)


def make_square_root_scaled_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = h5py.File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    brightness = f['apoapse/muv/dayside/detector/brightness'][:]

    if brightness.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:]
    tangent_altitude = f['apoapse/muv/dayside/bin_geometry/tangent_altitude'][:][..., 4]
    field_of_view = f['apoapse/integration/field_of_view'][:]
    solar_zenith_angle = f['apoapse/muv/dayside/bin_geometry/solar_zenith_angle'][:]

    solar_zenith_angle[tangent_altitude != 0] = np.nan

    if brightness.size == 0:
        return

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    try:
        rgb_image = pu.colorize.square_root_scale_detector_image(brightness, mask=mask) / 255
    except IndexError:
        return

    n_spatial_bins = rgb_image.shape[1]
    spatial_bin_centers = np.linspace(0.5, n_spatial_bins - 1, num=n_spatial_bins)

    fig, ax = setup_figure(swath_number[-1] + 1, 6)

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath
        n_integrations = np.sum(swath_indices)
        fov = field_of_view[swath_indices]
        x, y = pu.detector_image.make_swath_grid(fov, swath, n_spatial_bins, n_integrations)
        pu.detector_image.pcolormesh_rgb_detector_image(ax, rgb_image[swath_indices], x, y)

        # This will add a line at the terminator
        ax.contour(spatial_bin_centers + swath * pu.constants.angular_slit_width, fov, solar_zenith_angle[swath_indices], [90], colors='red', linewidths=0.5)

    ax.set_xlim(0, pu.constants.angular_slit_width * (swath_number[-1] + 1))
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_binning = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_binning = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = f'{orbit_code}-Ls{solar_longitude * 10:04.0f}-angle{subsolar_subspacecraft_angle * 10:04.0f}-binning{spatial_binning:04}x{spectral_binning:04}-sqrt-ql.png'

    plt.savefig(save_location / filename)
    plt.close()


def make_geometry_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = h5py.File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    latitude = f['apoapse/pixel_geometry/latitude'][:]
    longitude = f['apoapse/pixel_geometry/longitude'][:]

    if latitude.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:]
    field_of_view = f['apoapse/integration/field_of_view'][:]

    mars_map = pu.anc.load_map_mars_surface()

    print(np.nanmin(latitude), np.nanmax(latitude))
    print(np.nanmin(longitude), np.nanmax(longitude))
    print(latitude.shape, mars_map.shape)

    off_disk_mask = np.isnan(latitude)

    latitude[off_disk_mask] = 0
    longitude[off_disk_mask] = 0

    latitude_indices = np.floor((latitude + 90) * 10).astype('int')
    longitude_indices = np.floor(longitude * 10).astype('int')

    rgb_image = mars_map[latitude_indices.flatten(), longitude_indices.flatten(), :]
    rgb_image = np.reshape(rgb_image, latitude.shape + (4,))
    rgb_image[off_disk_mask] = 0

    fig, ax = setup_figure(swath_number[-1] + 1, 6)

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath
        n_integrations = np.sum(swath_indices)
        fov = field_of_view[swath_indices]
        x, y = pu.detector_image.make_swath_grid(fov, swath, 1024, n_integrations)
        pu.detector_image.pcolormesh_rgb_detector_image(ax, rgb_image[swath_indices], x, y)

    ax.set_xlim(0, pu.constants.angular_slit_width * (swath_number[-1] + 1))
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_binning = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_binning = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = f'{orbit_code}-Ls{solar_longitude * 10:04.0f}-angle{subsolar_subspacecraft_angle * 10:04.0f}-binning{spatial_binning:04}x{spectral_binning:04}-geometry-ql.png'

    plt.savefig(save_location / filename)
    plt.close()


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/home/kyle/iuvs/cloudspotting/')

    n_cpus = mp.cpu_count()
    pool = mp.Pool(n_cpus -1)

    #for orb in [3453]:
    #    pool.apply_async(func=make_histogram_equalized_detector_image, args=(orb,))
        #pool.apply_async(func=make_square_root_scaled_detector_image, args=(orb,))
        #pool.apply_async(func=make_geometry_detector_image, args=(orb,))
    make_histogram_equalized_detector_image(3453)
    pool.close()
    pool.join()
