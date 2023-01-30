import h5py
import numpy as np


def add_apsis_data_to_file(file: h5py.File, apsis_path: str, ephemeris_times: np.ndarray) -> None:
    file.require_group(apsis_path)
    # TODO: add ephemeris time
    # TODO: add mars year
    # TODO: add Ls
    # TODO: add sol
    # TODO: add subsolar latitude
    # TODO: add subsolar longitude
    # TODO: add subspacecraft latitude
    # TODO: add subspacecraft longitude
    # TODO: add subspacecraft altitude
    # TODO: add subspacecraft local time
    # TODO: add mars sun distance
    # TODO: add subsolar subspacecraft angle
    pass