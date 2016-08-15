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

# path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/'
path = '../../../data/csia/CASIA-WebFace/'
all_mods = {}
for people in os.listdir(path):
    for img in os.listdir(path + people):
        mod = img_model(path + '/' + people + '/' + img)
        if mod != "RGB":
            print path + '/' + people + '/' + img
        if all_mods.has_key(mod) == False:
            all_mods[mod] = 1
        else:
            all_mods[mod] += 1
print all_mods
