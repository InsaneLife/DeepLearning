# coding=utf-8
# author = 'AaronChou'

import random
import sys
import os


def walk_through_folder_for_split(src_folder):
    test_set = []
    train_set = []

    label = 0
    for people_folder in os.listdir(src_folder):
        people_path = src_folder + people_folder + '/'
        people_imgs = []
        for img_file in os.listdir(people_path):
            img_path = people_path + img_file
            people_imgs.append((img_path, label))
        # if len(people_imgs) < 25:
        #     continue
        random.shuffle(people_imgs)
        lens = people_imgs.__len__() - 1
        test_set += people_imgs[0:5]
        train_set += people_imgs[5:lens]

        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
        label += 1
    print ''
    print 'test  set num: %d' % (len(test_set))
    print 'train set num: %d' % (len(train_set))
    return test_set, train_set


def set_to_csv_file(data_set, file_name):
    f = open(file_name, 'wb')
    for item in data_set:
        line = item[0] + ',' + str(item[1]) + '\n'
        f.write(line)
    f.close()


if __name__ == '__main__':
    src_folder = 'E:/soft/Project/zte/ztedata/CBSR_webface/100_resize/'
    test_set_file = 'E:/soft/Project/zte/ztedata/CBSR_webface/test_100_set_file.csv'
    train_set_file = 'E:/soft/Project/zte/ztedata/CBSR_webface/train_100_set_file.csv'
    if not src_folder.endswith('/'):
        src_folder += '/'

    test_set, train_set = walk_through_folder_for_split(src_folder)
    set_to_csv_file(test_set, test_set_file)
    set_to_csv_file(train_set, train_set_file)
