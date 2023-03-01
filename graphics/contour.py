import numpy as np
import matplotlib.pyplot as plt


def add_terminator_contour_line_to_axis(axis: plt.Axes, solar_zenith_angle: np.ndarray, swath_number: np.ndarray,
                                        field_of_view: np.ndarray, angular_size: float) -> None:
    """Add terminator contour line to an axis.

    Parameters
    ----------
    axis
    solar_zenith_angle
    swath_number
    field_of_view
    angular_size

    Returns
    -------

    """
    n_spatial_bins = solar_zenith_angle.shape[1]
    spatial_bin_centers = np.arange(n_spatial_bins) + 0.5

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath
        axis.contour((spatial_bin_centers / n_spatial_bins + swath) * angular_size, field_of_view[swath_indices],
                     solar_zenith_angle[swath_indices], [90], colors='red', linewidths=0.5)
