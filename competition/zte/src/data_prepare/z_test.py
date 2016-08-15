#coding=utf8
from PIL import Image
import os
import shutil
import re

def resize_img(src_file_path, dest_file_path):
    im = Image.open(src_file_path)
    im.load()
    # print im



dest = "e:"

path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/0000254_004.jpg'
resize_img(path, dest)

path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/0000256_008.jpg'
path1 = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/'
resize_img(path, dest)
print len(os.listdir(path1))
