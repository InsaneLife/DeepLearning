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
path = 'E:/soft/Project/zte/ztedata/img/croped_images/'
all_mods = set()
# for img in os.listdir(path):
#     mod = img_model(path + img)
#     all_mods.add(mod)
#
# print all_mods

print img_model('E:/soft/Project/zte/ztedata/Img/croped_images/Alan_Rickman/Alan_Rickman_2936_1699.jpeg')
