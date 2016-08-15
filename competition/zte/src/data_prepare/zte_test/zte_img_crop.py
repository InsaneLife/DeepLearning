#!/usr/bin/env python
# -*- coding:utf8 -*-

from PIL import Image
import sys
import os
import numpy as np

def crop_img_by_half_center(src_file_path, dest_file_path):
    im = Image.open(src_file_path)
    x_size, y_size = im.size
    start_point_xy = x_size / 6
    end_point_xy = x_size*5 / 6
    box = (start_point_xy, start_point_xy, end_point_xy, end_point_xy)
    arr_img = np.asarray(im, dtype='float64')
    if im.mode == 'L':
        im.mode = 'RGB'

    new_im = im.crop(box)
    new_new_im = new_im.resize((47, 55))
    new_new_im.save(dest_file_path)


def walk_through_the_folder_for_crop(aligned_db_folder, result_folder):
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    i = 0
    img_count = 0

    for img_file in os.listdir(aligned_db_folder):
        src_img_path = aligned_db_folder + img_file
        dest_img_path = result_folder + img_file
        crop_img_by_half_center(src_img_path, dest_img_path)
    i += 1
    img_count += len(os.listdir(aligned_db_folder))
    sys.stdout.write('\rsub_folder: %d, imgs %d' % (i, img_count))
    sys.stdout.flush()
    print ''

if __name__ == '__main__':
    #aligned_db_folder = '/home/work/pictures'
    aligned_db_folder = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures/'
    result_folder =  'E:/soft/Project/zte/ztedata/zte_face_test/test1/pictures_copy/'
    if not aligned_db_folder.endswith('/'):
        aligned_db_folder += '/'
    if not result_folder.endswith('/'):
        result_folder += '/'
    #im = Image.open('E:\soft\Project\zte\ztedata\youtubeDataset\\aligned_images_DB\Aaron_Guiel\\5\\aligned_detect_5.1841.jpg')
    walk_through_the_folder_for_crop(aligned_db_folder, result_folder)
