import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from glob import glob

from system.utils import string_to_dict


class DirectoryService:
    def __init__(self):
        self.detail_files = ["\\sources\\install.esd", "\\sources\\install.wim", "\\sources\\boot.wim"]
        self.executor = ThreadPoolExecutor()

    @staticmethod
    def _is_empty(path):
        return len(os.listdir(path)) == 0

    def _get_source_filename(self, path):
        for filename in self.detail_files:
            if os.path.isfile(f"{path}{filename}"):
                return filename
        return

    def _is_windows_image(self, path):
        return any(os.path.isfile(f"{path}{file}") for file in self.detail_files)

    @staticmethod
    def get_children(path):
        return glob(path + '/*/')

    @property
    def main(self):
        return f"{os.getcwd()}\\"

    @property
    def has_windows_image(self):
        return self._is_windows_image(self.main)

    @property
    def windows_image_detail(self):
        return self.get_windows_image_details(paths=self.main)[0]

    @property
    def children(self):
        return glob(self.main + '/*/')

    @property
    def empty(self):
        return self._is_empty(self.main)

    @property
    def empty_children(self):
        return [child for child in self.children if self._is_empty(child)]

    def is_empty(self, path, path_only=False):
        if path_only:
            return self._is_empty(os.path.join(self.main, path))
        else:
            return self._is_empty(path)

    def create_directory(self, path):
        os.mkdir(os.path.join(self.main, path))
        return

    def move_files_and_folders(self, names, target_folder, path_only=False):
        if path_only:
            target_folder = os.path.join(self.main, target_folder)
            names = [os.path.join(self.main, name) for name in names]
        for name in names:
            if os.path.exists(name):
                shutil.move(name, target_folder)

    def get_windows_image_details(self, paths=None):
        details = []
        path_and_threads = []
        paths = self.children if not paths else paths
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            if not self._is_windows_image(path):
                continue
            detail_filename = self._get_source_filename(path)
            command = f"""dism /Get-WimInfo /WimFile:"{path}{detail_filename}" /index:1"""
            path_and_threads.append({path: self.executor.submit(subprocess.getoutput, command)})
        for path_and_thread in path_and_threads:
            (path, thread) = path_and_thread.popitem()
            details.append({path: string_to_dict(thread.result(), remove_last_line=True)})
        return details
