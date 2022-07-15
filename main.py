import hashlib
import shutil
import glob
import os
import re
from tkinter import image_names

from constants import SOURCE_FILE_PATH, DESTINATION_FILE_PATH, USB_DRIVE_CODE
from os import listdir

class HashingError(Exception):
    pass

def hash_image(image):
    assert os.path.isfile(image)
    with open(image,"rb") as f:
        bro = f.read()
        jim = hashlib.sha256(bro).hexdigest();
    return jim
        
def check_images(src_file_path):
    file_names = listdir(os.path.join(USB_DRIVE_CODE, src_file_path))
    # print(file_names)
    for name in file_names:
        if(os.path.isfile(os.path.join(USB_DRIVE_CODE, src_file_path, name))):
            src_hash = hash_image(os.path.join(USB_DRIVE_CODE, src_file_path, name))
            shutil.copy(os.path.join(USB_DRIVE_CODE, src_file_path, name), os.path.join(DESTINATION_FILE_PATH, src_file_path))
            dst_hash = hash_image(os.path.join(DESTINATION_FILE_PATH, src_file_path, name))
            if(src_hash != dst_hash):
                raise HashingError("Error! Something went wrong: " + os.path.join(DESTINATION_FILE_PATH, src_file_path, name))

def locate_scan_folders():
    # Looking for .jpg file types!
    folder_locations = []
    path = os.path.join(SOURCE_FILE_PATH, '\\**\\*.jpg')
    # print(path)
    image_locations = glob.glob(path, recursive=True)
    # print(image_locations) 
    for loc in image_locations:
        loc_str = loc.split("\\")
        loc_str.pop(len(loc_str) - 1)
        # print("loc_str: " + str(loc_str))
        # print("loc: " + loc)
        loc_str.pop(0)
        new_loc_str = ""
        index = 0
        while(True):
            new_loc_str = os.path.join(new_loc_str, loc_str[index])
            if not (os.path.exists(os.path.join(DESTINATION_FILE_PATH, new_loc_str))):
                os.mkdir(os.path.join(DESTINATION_FILE_PATH, new_loc_str))
                break
            if(index >= len(loc_str) - 1):
                break
            index += 1
        folder_locations.append(new_loc_str)
    locations_set = set(folder_locations)
    return (list(locations_set))

def make_copies():
    # locate_scan_folders()
    # print(SOURCE_FILE_PATH)
    # print(sorted(locate_scan_folders()))
    for loc in sorted(locate_scan_folders()):
        # print("Location: " + loc)
        check_images(loc)

make_copies()

# "H:\drone_data\36867 - Washington 1 - 2022-04-05\overview\Overview\1\110MEDIA\DJI_0504_R.JPG"