# coding=utf-8

from PIL import Image
import os
import shutil
import re


def resize_img(src_file_path, dest_file_path):
    im = Image.open(src_file_path)
    im.load()

    if im.mode == "RGB":
        new_Img = im.resize((47, 55))
        new_Img.save(dest_file_path)
        return 1
    else:
        return 0

def walk_through_the_folder_for_resize(resized_folder, target_folder):
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)

    i = 0
    max_person_num = 100000
    max_pic_num_every_person = 400
    min_pic_num_every_person = 25

    for people_folder in os.listdir(resized_folder):
        src_people_path = resized_folder + people_folder + '/'
        dest_people_path = target_folder + people_folder + '/'
        if not os.path.exists(dest_people_path):
            os.mkdir(dest_people_path)
        '''
        dest_people_path = dest_people_path + '0' + '/'
        if not os.path.exists(dest_people_path):
            os.mkdir(dest_people_path)
        '''
        j = 0
        available_Pic = 0

        if len(os.listdir(src_people_path)) < min_pic_num_every_person:
            os.rmdir(dest_people_path)
            continue
        for img in os.listdir(src_people_path):
            src_img = src_people_path + img
            dest_img = dest_people_path + img
            available_Pic += resize_img(src_img, dest_img)
            j += 1
            if j >= max_pic_num_every_person:
                break
        if available_Pic < min_pic_num_every_person:
            shutil.rmtree(dest_people_path)
            continue
        i += 1
        # debug
        if i >= max_person_num:
            break
    print i


if __name__ == '__main__':
    result_folder = 'E:/soft/Project/zte/ztedata/img/croped_images/'
    # actors
    walk_through_the_folder_for_resize('E:/soft/Project/zte/ztedata/ImgDataset/actors/faces/',
                                       result_folder)
    # actresses
    walk_through_the_folder_for_resize('E:/soft/Project/zte/ztedata/ImgDataset/actresses/faces/',
                                       result_folder)
