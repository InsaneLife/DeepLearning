# coding=utf-8
# author = 'AaronChou'
import os
import numpy as np
from PIL import Image


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def img_model(src_file_path):
    im = Image.open(src_file_path)
    im.load()

    arr_img = np.asarray(im, dtype='float64')
    arr_img = rgb2gray(arr_img)
    # print im
    print arr_img.shape
    return im.mode


path = '../../../data/csia/CASIA-WebFace//4572741/009.jpg' # L
path = '../../../data/csia/CASIA-WebFace//4572741/001.jpg' # RGB


img_model(path)

