import h5py


def add_pixel_geometry_data_to_file(file: h5py.File, pixel_geometry_path: str) -> None:
    file.require_group(pixel_geometry_path)
