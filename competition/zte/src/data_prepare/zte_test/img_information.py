# coding=utf8
from PIL import Image
import os
import shutil
import re


def img_model(src_file_path):
    im = Image.open(src_file_path)
    im.load()
    # print im
    return im.mode

# mode 有"L", "RGBX", "RGBA", "CMYK"

path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/'
all_mods = set()
for img in os.listdir(path):
    mod = img_model(path + img)
    all_mods.add(mod)

mods_map = {}
for mod in all_mods:
    num = 0
    for img in os.listdir(path):
        if img_model(path + img) == mod:
            num += 1
    mods_map[mod] = num

print mods_map
