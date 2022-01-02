from slugify import slugify

from system.services import DirectoryService
from system.utils import get_last_item_from_path


class BootableUSB:
    service = DirectoryService()

    def __init__(self):
        self.default_folder_name = "%(Name)s_%(Architecture)s_%(Languages)s_%(Created)s"
        self.windows_image_details = self.service.get_windows_image_details()
        self.media_files = ['sources', 'support', 'efi', 'boot', 'upgrade', 'autorun.inf', 'bootmgr', 'bootmgr.efi',
                            'setup.exe', 'Boot', 'EFI', 'en-us', 'HBCD_PE.ini', 'Version.txt']
        self.visible_keys = ["Name", "Architecture", "Created", "Languages"]

    def run(self):
        self._show_current_media(line_break=True)
        media_choice = self._get_media_choice()
        if self.service.has_windows_image:
            if self.service.empty_children:
                target_folder_name = self._get_empty_folder_choice()
                target_folder_name = target_folder_name if target_folder_name else self._get_empty_folder_name()
            else:
                target_folder_name = self._get_empty_folder_name()
            self.service.move_files_and_folders(self.media_files, target_folder_name, path_only=True)
        if media_choice:
            media_files = [f"{list(media_choice.keys())[0]}{media_file}" for media_file in self.media_files]
            self.service.move_files_and_folders(media_files, self.service.main)
        self._show_current_media()

    @property
    def _default_folder_name(self):
        return slugify(self.default_folder_name % {**list(self.service.windows_image_detail.values())[0]})

    def _show_current_media(self, line_break=False):
        if self.service.has_windows_image:
            (path, detail) = self.service.windows_image_detail.popitem()
            visible_detail = '({})'.format(', '.join([detail.get(key) for key in self.visible_keys]))
            print(f"✓ Current media choice: {visible_detail}" + ("\n" if line_break else ''))

    def _get_media_choice(self):
        choice = None
        if not self.windows_image_details:
            print("No selectable media found.\n")
            return

        print("Select the media you want to set bootable: ")
        for index, image in enumerate(self.windows_image_details, start=1):
            (path, detail) = image.copy().popitem()
            visible_detail = '({})'.format(', '.join([detail.get(key) for key in self.visible_keys]))
            print(f"{index}. {get_last_item_from_path(path)} {visible_detail}")

        while choice not in range(1, len(self.windows_image_details) + 1):
            try:
                choice = int(input("Choice: "))
            except ValueError:
                choice = None
        print()
        return self.windows_image_details[choice - 1]

    def _get_empty_folder_choice(self):
        choice = None
        empty_children = self.service.empty_children
        empty_children.append("Create new folder")
        print("Select a folder to move existed media files to there: ")
        for index, path in enumerate(empty_children, start=1):
            print(f"{index}. {get_last_item_from_path(path)}")
        while choice not in range(1, len(empty_children) + 1):
            try:
                choice = int(input("Choice: "))
            except ValueError:
                choice = None
        print()
        return empty_children[choice - 1] if choice != len(empty_children) else None

    def _get_empty_folder_name(self):
        folder_name = None
        print("Enter a folder name to move existed media files to there: ")
        while not folder_name:
            try:
                folder_name = input("Folder name: ")
                if not folder_name:
                    folder_name = self._default_folder_name
                self.service.create_directory(folder_name)
            except FileExistsError:
                if not self.service.is_empty(folder_name, path_only=True):
                    print("This folder already exists and not empty.")
                    folder_name = None
        print()
        return folder_name


if __name__ == "__main__":
    busb = BootableUSB()
    busb.run()
    input("Press enter to close the window.")
