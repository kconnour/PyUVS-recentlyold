from h5py import File
from netCDF4 import Dataset
import numpy as np

import extract
from radprop import get_particle_sizes, get_wavelengths, get_scattering_cross_section, get_extinction_cross_section


def make_latitude_centers(gcm: Dataset) -> np.ndarray:
    return extract.get_latitude_centers(gcm)


def make_latitude_edges(gcm: Dataset) -> np.ndarray:
    latitude = make_latitude_centers(gcm)
    return np.linspace(-90, 90, num=latitude.shape[0] + 1)


def make_longitude_centers(gcm: Dataset) -> np.ndarray:
    return extract.get_longitude_centers(gcm)


def make_longitude_edges(gcm: Dataset) -> np.ndarray:
    longitude = make_longitude_centers(gcm)
    return np.linspace(0, 360, num=longitude.shape[0] + 1)


def make_simulation_sol_centers(gcm: Dataset) -> np.ndarray:
    return extract.get_simulation_sol_centers(gcm)


def make_simulation_sol_edges(gcm: Dataset) -> np.ndarray:
    return np.unique(extract.get_simulation_sol_edges(gcm))


def make_yearly_sol_centers(gcm: Dataset) -> np.ndarray:
    sol_centers = make_simulation_sol_centers(gcm)
    return np.mod(sol_centers, 668)


def make_yearly_sol_edges(gcm: Dataset) -> np.ndarray:
    sol_edges = make_simulation_sol_edges(gcm)
    return np.mod(sol_edges, 668)


def make_local_time_centers(gcm: Dataset) -> np.ndarray:
    return extract.get_local_time_centers(gcm)


def make_local_time_edges(gcm: Dataset) -> np.ndarray:
    return extract.get_local_time_edges(gcm)


def make_solar_longitude_centers(gcm: Dataset) -> np.ndarray:
    areo = extract.get_areo(gcm)
    return np.mod(np.squeeze(areo), 360)


def make_ak(gcm: Dataset) -> np.ndarray:
    return extract.get_ak(gcm)


def make_bk(gcm: Dataset) -> np.ndarray:
    return extract.get_bk(gcm)


def make_surface_temperature(gcm: Dataset) -> np.ndarray:
    return extract.get_surface_temperature(gcm)


def make_surface_pressure(gcm: Dataset) -> np.ndarray:
    return extract.get_surface_pressure(gcm)


def make_atmospheric_temperature(gcm: Dataset) -> np.ndarray:
    temperature = extract.get_atmospheric_temperature(gcm)
    return np.moveaxis(temperature, 2, -1)


def make_atmospheric_pressure(gcm: Dataset) -> np.ndarray:
    surface_pressure = make_surface_pressure(gcm)
    ak = make_ak(gcm)
    bk = make_bk(gcm)
    return np.multiply.outer(surface_pressure, bk) + ak


def make_dust_optical_depth(gcm: Dataset, radprop: File, target_wavelength: float, reference_wavelength: float = 0.690) -> np.ndarray:
    atmospheric_pressure = make_atmospheric_pressure(gcm)

    radprop_particle_sizes = get_particle_sizes(radprop)
    radprop_wavelengths = get_wavelengths(radprop)
    radprop_extinction_cross_section = get_extinction_cross_section(radprop)

    simulation_extinction_optical_depth = extract.get_extinction_dust_opacity_per_pascal(gcm)
    simulation_extinction_optical_depth = np.moveaxis(simulation_extinction_optical_depth, 2, -1)
    # TODO: they don't currently give me particle size info so I'm assuming a constant value. In the future, I should
    #  use the values they give me instead of making up values
    simulation_particle_sizes = np.ones(simulation_extinction_optical_depth.shape) * 1.2

    scaled_optical_depth = _scale_optical_depth(
        simulation_extinction_optical_depth, simulation_particle_sizes, reference_wavelength,
        radprop_extinction_cross_section, radprop_particle_sizes, radprop_wavelengths, target_wavelength)

    return _compute_optical_depth(atmospheric_pressure, scaled_optical_depth)


def make_ice_optical_depth(gcm: Dataset, radprop: File, target_wavelength: float, reference_wavelength: float = 12) -> np.ndarray:
    atmospheric_pressure = make_atmospheric_pressure(gcm)

    radprop_particle_sizes = get_particle_sizes(radprop)
    radprop_wavelengths = get_wavelengths(radprop)
    radprop_extinction_cross_section = get_extinction_cross_section(radprop)
    radprop_scattering_cross_section = get_scattering_cross_section(radprop)

    simulation_absorption_optical_depth = extract.get_absorption_ice_opacity_per_pascal(gcm)
    simulation_absorption_optical_depth = np.moveaxis(simulation_absorption_optical_depth, 2, -1)
    # TODO: they don't currently give me particle size info so I'm assuming a constant value. In the future, I should
    #  use the values they give me instead of making up values
    simulation_particle_sizes = np.ones(simulation_absorption_optical_depth.shape) * 1.5  # For now...

    # Convert absorption optical depth to extinction
    reference_wavelength_index = _get_closest_index(radprop_wavelengths, reference_wavelength)
    factor = radprop_extinction_cross_section[:, reference_wavelength_index] / \
          (radprop_extinction_cross_section[:, reference_wavelength_index] - radprop_scattering_cross_section[:, reference_wavelength_index])
    absorption_to_extinction_factor = np.interp(simulation_particle_sizes, radprop_particle_sizes, factor)
    simulation_extinction_optical_depth = simulation_absorption_optical_depth * absorption_to_extinction_factor

    scaled_optical_depth = _scale_optical_depth(
        simulation_extinction_optical_depth, simulation_particle_sizes, reference_wavelength,
        radprop_extinction_cross_section, radprop_particle_sizes, radprop_wavelengths, target_wavelength)

    return _compute_optical_depth(atmospheric_pressure, scaled_optical_depth)


def _get_closest_index(array: np.ndarray, value: float) -> int:
    return np.abs(array - value).argmin()


def _scale_optical_depth(
        simulation_optical_depth: np.ndarray,
        simulation_particle_sizes: np.ndarray,
        simulation_reference_wavelength: float,
        radprop_extinction_cross_section: np.ndarray,
        radprop_particle_sizes: np.ndarray,
        radprop_wavelengths: np.ndarray,
        target_wavelength: float) -> np.ndarray:

    target_wavelength_index = _get_closest_index(radprop_wavelengths, target_wavelength)
    reference_wavelength_index = _get_closest_index(radprop_wavelengths, simulation_reference_wavelength)

    target_cext = radprop_extinction_cross_section[:, target_wavelength_index]
    reference_cext = radprop_extinction_cross_section[:, reference_wavelength_index]

    scaling_factor = np.interp(simulation_particle_sizes, radprop_particle_sizes, target_cext / reference_cext)
    return simulation_optical_depth * scaling_factor


def _compute_optical_depth(simulation_pressure: np.ndarray, simulation_optical_depth: np.ndarray) -> np.ndarray:
    p_diff = np.diff(simulation_pressure, axis=-1)
    return np.sum(simulation_optical_depth * p_diff, axis=-1)
