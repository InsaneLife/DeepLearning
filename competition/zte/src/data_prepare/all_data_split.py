#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import random


def merge_set(test_set_file_youtube, test_set_file_img):
    i = 0
    test_set = []
    f = open(test_set_file_youtube)
    read = f.readlines()
    f.close()
    mark = 0
    for each in read:
        test_set.append(each)
        each = each[:-1].split(",")
        if each[1] != mark:
            i += 1
            mark = each[1]
    # i = 1595
    f = open(test_set_file_img)
    read = f.readlines()
    f.close()
    mark = '0'
    for each in read:
        each = each[:-1].split(",")
        if each[1] != mark:
            i += 1
            mark = each[1]
        test_set.append(each[0] + "," + str(i) + "\n")
    return test_set


def write_to_file(set, set_file):
    f = open(set_file, 'wb')
    for each in set:
        f.write(each)
    f.close()


if __name__ == '__main__':
    test_set_file_youtube = 'E:/soft/Project/zte/ztedata/youtube/test_set_file.csv'
    train_set_file_youtube = 'E:/soft/Project/zte/ztedata/youtube/train_set_file.csv'
    test_set_file_img = 'E:/soft/Project/zte/ztedata/img/test_set_file.csv'
    train_set_file_img = 'E:/soft/Project/zte/ztedata/img/train_set_file.csv'

    test_set_file = 'E:/soft/Project/zte/ztedata/youtube_and_img/test_set_file.csv'
    train_set_file = 'E:/soft/Project/zte/ztedata/youtube_and_img/train_set_file.csv'

    test_set = merge_set(test_set_file_youtube, test_set_file_img)  # [["file ,mark"]]
    write_to_file(test_set, test_set_file)

    train_set = merge_set(train_set_file_youtube, train_set_file_img)
    write_to_file(train_set, train_set_file)
