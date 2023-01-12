from iuvs_data_files import DataFinder
from structure import DataFile


class Group:
    def __init__(self, data_file: DataFile, data_finder: DataFinder, group_path: str):
        self.data_file = data_file
        self.data_finder = data_finder
        self.group_path = group_path

    def _make_dataset_path(self, name: str):
        return f'{self.group_path}/{name}'