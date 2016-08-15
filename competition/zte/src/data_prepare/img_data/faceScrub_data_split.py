#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import random
from math import ceil
import sys


def walk_through_folder_for_split(src_folder):
    test_set = []
    train_set = []

    label = 0

    for people_folder in os.listdir(src_folder):
        people_path = src_folder + people_folder + '/'
        people_imgs = []
        for img in os.listdir(people_path):
            img_path = people_path + img
            people_imgs.append((img_path, label))
        if len(people_imgs) < 25:
            continue
        random.shuffle(people_imgs)
        '''
        idx = int(ceil(len(people_imgs) / 5))
        test_set += people_imgs[0:idx]
        train_set += people_imgs[idx:]
        '''

        idx = len(people_imgs)/5
        end = idx*5-1
        test_set += people_imgs[0:5]
        train_set += people_imgs[5:25]

        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
        label += 1
    print '\ntest set num: %d' % (len(test_set))
    print 'train set num: %d' % (len(train_set))
    return test_set, train_set


def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()


if __name__ == '__main__':
    src_folder = 'E:/soft/Project/zte/ztedata/img/croped_images/'
    test_set_file = 'E:/soft/Project/zte/ztedata/img/test_set_file.csv'
    train_set_file = 'E:/soft/Project/zte/ztedata/img/train_set_file.csv'
    test_set, train_set = walk_through_folder_for_split(src_folder)
    set_to_csv_file(test_set, test_set_file)
    set_to_csv_file(train_set, train_set_file)
