import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from glob import glob

from system.exceptions import AdminPrivilegesException
from system.utils import string_to_dict


class DirectoryService:

    @staticmethod
    def _is_empty(path=None):
        return len(os.listdir(path)) == 0

    @staticmethod
    def get_children(path):
        return glob(path + '/*/')

    @staticmethod
    def move_files_and_folders(files, target_folder):
        for file in files:
            if os.path.exists(file):
                shutil.move(file, target_folder)

    @staticmethod
    def create_directory(path):
        os.mkdir(path)

    @property
    def working_directory(self):
        return f"{os.getcwd()}\\"

    @property
    def children(self):
        return glob(self.working_directory + '/*/')

    @property
    def empty(self):
        return self._is_empty()

    @property
    def empty_children(self):
        return [child for child in self.children if self.is_empty(child)]

    def is_empty(self, path):
        return self._is_empty(path)
