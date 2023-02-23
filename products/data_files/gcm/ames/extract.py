from netCDF4 import Dataset
import numpy as np

from ames.algorithms import make_latitude_edges, make_longitude_edges, make_yearly_sol_from_simulation_sol, \
    make_solar_longitude, make_pressure


def get_latitude_centers(gcm: Dataset) -> np.ndarray:
    return gcm['lat'][:]


def get_latitude_edges(gcm: Dataset) -> np.ndarray:
    latitude = get_latitude_centers(gcm)
    return make_latitude_edges(latitude)


def get_longitude_centers(gcm: Dataset) -> np.ndarray:
    return gcm['lon'][:]


def get_longitude_edges(gcm: Dataset) -> np.ndarray:
    longitude = get_longitude_centers(gcm)
    return make_longitude_edges(longitude)


def get_simulation_sol_centers(gcm: Dataset) -> np.ndarray:
    return gcm['time'][:]


def get_simulation_sol_edges(gcm: Dataset) -> np.ndarray:
    return np.unique(gcm['time_bnds'][:])


def get_yearly_sol_centers(gcm: Dataset) -> np.ndarray:
    simulation_sol_centers = get_simulation_sol_centers(gcm)
    return make_yearly_sol_from_simulation_sol(simulation_sol_centers)


def get_yearly_sol_edges(gcm: Dataset) -> np.ndarray:
    simulation_sol_edges = get_simulation_sol_edges(gcm)
    return make_yearly_sol_from_simulation_sol(simulation_sol_edges)


def get_local_time_centers(gcm: Dataset) -> np.ndarray:
    return gcm['time_of_day_24'][:]


def get_local_time_edges(gcm: Dataset) -> np.ndarray:
    return gcm['time_of_day_edges_24'][:]


def get_areo(gcm: Dataset) -> np.ndarray:
    return gcm['areo'][:, :, 0]


def get_solar_longitude_centers(gcm: Dataset) -> np.ndarray:
    areo = get_areo(gcm)
    return make_solar_longitude(areo)


def get_ak(gcm: Dataset) -> np.ndarray:
    return gcm['pk'][:]   # John says that pk is the same thing as ak


def get_bk(gcm: Dataset) -> np.ndarray:
    return gcm['bk'][:]


def get_surface_pressure(gcm: Dataset) -> np.ndarray:
    return gcm['ps'][:]


def get_surface_temperature(gcm: Dataset) -> np.ndarray:
    return gcm['ts'][:]


def get_atmospheric_temperature(gcm: Dataset) -> np.ndarray:
    temperature = gcm['temp'][:]
    return np.moveaxis(temperature, 2, -1)


def get_atmospheric_pressure(gcm: Dataset) -> np.ndarray:
    ak = get_ak(gcm)
    bk = get_bk(gcm)
    surface_pressure = get_surface_pressure(gcm)
    return make_pressure(surface_pressure, ak, bk)
