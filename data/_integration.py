import numpy as np

from iuvs_data_files import DataFinder
from structure import DataFile
from _data_versions import current_file_is_up_to_date, get_latest_pipeline_versions
from _group import Group


comment = 'Taken from the integration structure from v13 of the IUVS data products'

class Integration(Group):
    def __init__(self, data_file: DataFile, data_finder: DataFinder, group_path: str):
        super().__init__(data_file, data_finder, group_path)

    def add_ephemeris_time(self):
        name = 'ephemeris_time'
        dataset_path = self._make_dataset_path(name)
        if not current_file_is_up_to_date(self.data_file, dataset_path):
            data = np.concatenate([f['integration'].data['et'] for f in self.data_finder.hduls])
            dataset = self.data_file.file[self.group_path].create_dataset(name, data=data)
            dataset.attrs['units'] = 'Seconds since J2000'
            dataset.attrs['version'] = get_latest_pipeline_versions()[name]
            dataset.attrs['comment'] = comment

    def add_field_of_view(self):
        name = 'field_of_view'
        dataset_path = self._make_dataset_path(name)
        if not current_file_is_up_to_date(self.data_file, dataset_path):
            data = np.concatenate([f['integration'].data['fov_deg'] for f in self.data_finder.hduls])
            dataset = self.data_file.file[self.group_path].create_dataset(name, data=data)
            dataset.attrs['units'] = 'Degrees'
            dataset.attrs['version'] = get_latest_pipeline_versions()[name]
            dataset.attrs['comment'] = comment
