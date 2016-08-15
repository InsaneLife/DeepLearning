#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random
from PIL import Image


def walk_through_folder_for_split(src_folder):
    label = 0
    rgb_imgs = []
    l_imgs = []
    for img_file in os.listdir(src_folder):
        img_path = src_folder + img_file
        im = Image.open(img_path)
        if im.mode == 'RGB':
            rgb_imgs.append((img_path, label))
        elif im.mode == 'L':


            l_imgs.append((img_path, label))
        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
        label += 1
    print ''
    print 'test  set num: %d' % (len(rgb_imgs))
    return rgb_imgs, l_imgs


def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()


if __name__ == '__main__':
    # split RGB and L
    src_folder =  'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/'
    rgb_set_file =  'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file.csv'
    l_set_file =  'E:/soft/Project/zte/ztedata/zte_face_test/test1/l_set_file.csv'
    if not src_folder.endswith('/'):
        src_folder += '/'

    rgb_img_set, l_img_set = walk_through_folder_for_split(src_folder)
    set_to_csv_file(rgb_img_set, rgb_set_file)
    set_to_csv_file(l_img_set, l_set_file)

