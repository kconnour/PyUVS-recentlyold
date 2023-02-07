import mer
import numpy as np
import spiceypy

from . import spice


def get_ephemeris_time(ephemeris_times: np.ndarray, orbit: int) -> np.ndarray:
    return np.array([ephemeris_times[orbit - 1]])


def compute_mars_year(ephemeris_time: float) -> np.ndarray:
    utc = spiceypy.et2datetime(ephemeris_time)
    return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_whole_mars_year()])


def compute_solar_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_solar_longitude(ephemeris_time)])


def compute_sol(ephemeris_time: float) -> np.ndarray:
    utc = spiceypy.et2datetime(ephemeris_time)
    return np.array([mer.EarthDateTime(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second).to_sol()])


def compute_subsolar_latitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subsolar_point(ephemeris_time)[0]])


def compute_subsolar_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subsolar_point(ephemeris_time)[1]])


def compute_subspacecraft_latitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_point(ephemeris_time)[1]])


def compute_subspacecraft_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_point(ephemeris_time)[1]])


def compute_subspacecraft_altitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_altitude(ephemeris_time)])


def compute_subspacecraft_local_time(ephemeris_time: float, longitude: np.ndarray) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_local_time(ephemeris_time, np.radians(longitude))])


def compute_mars_sun_distance(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_mars_sun_distance(ephemeris_time)])



