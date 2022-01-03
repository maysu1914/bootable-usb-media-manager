# bootable-usb-media-manager
Makes it easy to manage Windows Installation media files in the bootable USB.

# the scenario
I have a bootable USB that has installation media files of operating systems in it (windows). All the OS files have their own folder, when I want to install one, I move the current OS files to its folder from the root directory and move the new OS files to the root directory of the USB.

this is the place where the project comes useful. It scans the root directory and reads all files of OSes (extracts the info from them) and the user selects the OS, it moves the current OS files to its own folder (or you can create a new folder) and moves the new OS files to the root directory.

you need admin privileges to run this project (because of the dism usage) (or use executable, it has a prompt for the admin privileges)

## this is my usb's root directory:
![usb root directory](https://raw.githubusercontent.com/maysu1914/bootable-usb-media-manager/readme/readme_files/usb_root.jpg)

## first page of the project:
![first page](https://raw.githubusercontent.com/maysu1914/bootable-usb-media-manager/readme/readme_files/cmd_1.jpg)

## media selection and existed media's folder:
![existed media folder](https://raw.githubusercontent.com/maysu1914/bootable-usb-media-manager/readme/readme_files/cmd_2_a.jpg)

## you can create new folder for it:
![existed media folder new](https://raw.githubusercontent.com/maysu1914/bootable-usb-media-manager/readme/readme_files/cmd_2_b.jpg)

## success page:
![success](https://raw.githubusercontent.com/maysu1914/bootable-usb-media-manager/readme/readme_files/cmd_3.jpg)
