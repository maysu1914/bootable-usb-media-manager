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


class WindowsImageService:
    executor = ThreadPoolExecutor()

    def __init__(self, *args, **kwargs):
        self.detail_files = ["\\sources\\install.esd", "\\sources\\install.wim", "\\sources\\boot.wim"]
        self.media_files = ['sources', 'support', 'efi', 'boot', 'upgrade', 'autorun.inf', 'bootmgr', 'bootmgr.efi',
                            'setup.exe']
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_source_filename(self, path):
        for filename in self.detail_files:
            if os.path.isfile(f"{path}{filename}"):
                return filename
        return

    def is_windows_image(self, path):
        return any(os.path.isfile(f"{path}{file}") for file in self.detail_files)

    def _get_windows_image_detail(self, path):
        if not self.is_windows_image(path):
            return
        detail_filename = self._get_source_filename(path)
        command = f"""dism /Get-WimInfo /WimFile:"{path}{detail_filename}" /index:1"""
        output = subprocess.getoutput(command)
        if string_to_dict(output).get("Error"):
            raise AdminPrivilegesException(output, "Run the application with admin privileges.")
        return output

    def get_windows_image_details(self, paths):
        details = []
        path_and_threads = []
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            path_and_threads.append({path: self.executor.submit(self._get_windows_image_detail, path)})
        for path_and_thread in path_and_threads:
            (path, thread) = path_and_thread.popitem()
            detail = thread.result()
            if detail:
                details.append({path: string_to_dict(detail, remove_last_line=True)})
        return details
