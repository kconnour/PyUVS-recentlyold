import numpy as np
from scipy.interpolate import interp1d

from .spice import compute_lat_lon_point


def extrapolate_bin_pixel_vector_to_native_vector(pixel_vector: np.ndarray, spatial_bin_edges: np.ndarray) -> np.ndarray:
    # shape: (n_integrations, n_spatial_bins, 5, 3)
    spatial_bin_center = (spatial_bin_edges[:-1] + spatial_bin_edges[1:]) / 2
    f = interp1d(spatial_bin_center, pixel_vector[:, :, 4, :], kind='linear', axis=1, fill_value='extrapolate')
    return f(np.arange(1024) + 0.5)


def make_along_slit_lat_lon(bin_vector: np.ndarray, spatial_bin_edges: np.ndarray, ephemeris_time: np.ndarray) -> \
        tuple[np.ndarray, np.ndarray]:
    bin_vector = extrapolate_bin_pixel_vector_to_native_vector(bin_vector, spatial_bin_edges)
    bin_vector = np.moveaxis(np.moveaxis(bin_vector, -1, 0) / np.sum(bin_vector, axis=-1), 0, -1)

    latitude = np.zeros(bin_vector.shape[:-1]) * np.nan
    longitude = np.zeros(bin_vector.shape[:-1]) * np.nan

    for integration in range(bin_vector.shape[0]):
        for spatial_bin in range(bin_vector.shape[1]):
            lat, lon = compute_lat_lon_point(ephemeris_time[integration], bin_vector[integration, spatial_bin, :])
            latitude[integration, spatial_bin] = lat
            longitude[integration, spatial_bin] = lon

    return latitude, longitude
