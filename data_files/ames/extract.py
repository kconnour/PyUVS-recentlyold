from netCDF4 import Dataset
import numpy as np


def get_latitude_centers(gcm: Dataset) -> np.ndarray:
    return gcm['lat'][:]


def get_longitude_centers(gcm: Dataset) -> np.ndarray:
    return gcm['lon'][:]


def get_simulation_sol_centers(gcm: Dataset) -> np.ndarray:
    return gcm['time'][:]


def get_simulation_sol_edges(gcm: Dataset) -> np.ndarray:
    return gcm['time_bnds'][:]


def get_local_time_centers(gcm: Dataset) -> np.ndarray:
    return gcm['time_of_day_24'][:]


def get_local_time_edges(gcm: Dataset) -> np.ndarray:
    return gcm['time_of_day_edges_24'][:]


def get_areo(gcm: Dataset) -> np.ndarray:
    return gcm['areo'][:]


def get_ak(gcm: Dataset) -> np.ndarray:
    return gcm['pk'][:]   # John says that pk is the same thing as ak


def get_bk(gcm: Dataset) -> np.ndarray:
    return gcm['bk'][:]


def get_surface_pressure(gcm: Dataset) -> np.ndarray:
    return gcm['ps'][:]


def get_surface_temperature(gcm: Dataset) -> np.ndarray:
    return gcm['ts'][:]


def get_atmospheric_temperature(gcm: Dataset) -> np.ndarray:
    return gcm['temp'][:]


def get_extinction_dust_opacity_per_pascal(gcm: Dataset) -> np.ndarray:
    return gcm['dustref'][:]


def get_absorption_ice_opacity_per_pascal(gcm: Dataset) -> np.ndarray:
    return gcm['cldref'][:]
