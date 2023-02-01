import warnings

import numpy as np

from pyuvs.typing import hdulist


def get_spatial_bin_edges(hduls: hdulist) -> np.ndarray:
    return np.append(hduls[0]['binning'].data['spapixlo'][0], hduls[0]['binning'].data['spapixhi'][0, -1] + 1) if hduls else np.array([])


def get_spectral_bin_edges(hduls: hdulist) -> np.ndarray:
    return np.append(hduls[0]['binning'].data['spepixlo'][0], hduls[0]['binning'].data['spepixhi'][0, -1] + 1) if hduls else np.array([])


def get_bin_width(bin_edges: np.ndarray) -> int:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            width = int(np.median(np.diff(bin_edges)))
    except ValueError:
        width = 0
    return width
