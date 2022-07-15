import hashlib
import shutil
import glob
import os

from constants import SOURCE_FILE_PATH, DESTINATION_FILE_PATH, USB_DRIVE_CODE
from os import listdir

class HashingError(Exception):
    pass

def hash_image(image):
    with open(image,"rb") as f:
        bro = f.read()
        jim = hashlib.sha256(bro).hexdigest();
    return jim
        
def check_images(src_file_path):
    file_names = listdir(USB_DRIVE_CODE + "\\" + src_file_path)
    print(file_names)
    for name in file_names:
        src_hash = hash_image(USB_DRIVE_CODE + "\\" + src_file_path + "\\" + name)
        shutil.copyfile(USB_DRIVE_CODE + "\\" +src_file_path + "\\" + name, DESTINATION_FILE_PATH + "\\" + src_file_path)
        dst_hash = hash_image(DESTINATION_FILE_PATH + "\\" + src_file_path + "\\" + name)
        if(src_hash != dst_hash):
            raise HashingError("Error! Something went wrong: " + DESTINATION_FILE_PATH + "\\" + src_file_path + "\\" + name)

def locate_scan_folders(file_path):
    # Looking for .jpg file types!
    folder_locations = []
    image_locations = glob.glob(file_path + '/**/*.jpg', recursive=True)  
    for loc in image_locations:
        loc_str = loc.split("\\")
        loc_str.pop(len(loc_str) - 1)
        loc_str.pop(0)
        new_loc_str = ""
        index = 0
        while(True):
            new_loc_str += loc_str[index]
            if not (os.path.exists(DESTINATION_FILE_PATH + "\\" + new_loc_str)):
                os.mkdir(DESTINATION_FILE_PATH + "\\" + new_loc_str)
                break
            if(index >= len(loc_str) - 1):
                break
            new_loc_str += "\\"
            index += 1
        folder_locations.append(new_loc_str)
    locations_set = set(folder_locations)
    return (list(locations_set))

def make_copies():
    # print(sorted(locate_scan_folders(SOURCE_FILE_PATH)))
    for loc in sorted(locate_scan_folders(SOURCE_FILE_PATH)):
        print("Location: " + loc)
        check_images(loc)

make_copies()