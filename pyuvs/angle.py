import numpy as np


def haversine(target_lat, target_lon, lat_array, lon_array):
    """

    Parameters
    ----------
    target_lat: float
        The latitude of the target point
    target_lon: float
        The longitude of the target point
    lat_array: np.ndarray
        The array of latitudes
    lon_array: np.ndarray
        The array of longitudes

    Returns
    -------
    distance: np.ndarray
        The distance between the point and the grid
    """
    # Calculate the angular distance between the target point and the array of coordinates
    d_lat = np.radians(lat_array - target_lat)
    d_lon = np.radians(lon_array - target_lon)

    # Turn that angular distance into a physical distance
    a = np.sin(d_lat / 2) ** 2 + np.cos(np.radians(target_lat)) * np.cos(np.radians(lat_array)) * np.sin(d_lon / 2) ** 2
    angle = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(angle)
