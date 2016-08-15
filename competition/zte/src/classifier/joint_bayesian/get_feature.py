__author__ = 'AaronChou'
# coding=utf-8
import cPickle
import os
import numpy as np


def get_each_pkl_data(path, data_set):
    """

    :param path:
    :param data_set:
    :return:[[vector,label]]
    """
    f = open(path, 'rb')
    vector, label = cPickle.load(f)
    f.close()
    for i in range(0, len(vector)):
        data_set.append([vector[i], label[i]])
    # print label[len(label)-1]
    return data_set


def get_pkl_data(folder):
    """

    :param folder:
    :return:[[vector,label]]
    """
    files = os.listdir(folder)
    data_set = []
    for file in files:
        file_path = folder + file
        data_set = get_each_pkl_data(file_path, data_set)

    return data_set


def get_pca_data(folder):
    data_set = get_pkl_data(folder)
    data = []
    label = []
    for each in data_set:
        data.append(each[0])
        label.append(each[1])
    return data, label


def get_train_data(folder):
    # path = 'E:/soft/Project/zte/ztedata/youtube/result_folder/31.pkl'
    # get_each_train_data(path, [])
    train_set = get_pkl_data(folder)
    train_map = {}  # key = personnum, value = each person's 20 pictures' vector
    for each in train_set:
        # each = [[vector, label]]
        if train_map.has_key(each[1]) == 0:
            train_map[each[1]] = []
        train_map[each[1]].append(each[0])
    train_vector = []
    train_label = []
    last_key = 0
    for key in train_map:
        # each person has 19 positive class
        for i in range(1, len(train_map[key])):
            vector_2 = np.vstack((train_map[key][i - 1], train_map[key][i]))
            train_vector.append(vector_2)
            train_label.append(1)
            i += 2
        # each person has 20 negative class
        for i in range(0, len(train_map[key])):
            if last_key != 0:
                vector_2 = np.vstack((train_map[last_key][i], train_map[key][i]))
                train_vector.append(vector_2)
                train_label.append(0)
        last_key = key
    return train_vector, train_label


def read_file(path):
    f = open(path)
    read = f.readlines()
    f.close()
    return read


def get_zte_rgb_test(zte_datalist, zte_rgb, test_folder):
    test_intra = []
    test_extra = []
    all_rgb_data = []
    pkl_set = get_pkl_data(test_folder)  # [[vector,label]]
    pkl_map = {}  # [key = label, value = vector]
    for each in pkl_set:
        pkl_map[each[1]] = each[0]

    datalist = read_file(zte_datalist)
    rgb_set = read_file(zte_rgb)
    rgb_map = {}  # [key = filename, value = label]
    for each in rgb_set:
        # get file name, such as 0000045_005
        file_name = each.split(',')[0].split('/')[each.split(',')[0].split('/').__len__() - 1].split('.')[0]
        rgb_map[file_name] = each.strip('\r\n').split(',')[1]
    index = 0
    for each in datalist:
        eachs = each.strip('\r\n').split(':')
        label = int(eachs[2])
        # get file name, such as 0000045_005
        img1_name = eachs[0].split('/')[1].split(".")[0]
        img2_name = eachs[1].split('/')[1].split(".")[0]

        if rgb_map.has_key(img1_name) and rgb_map.has_key(img2_name):
            all_rgb_data.append(pkl_map[int(rgb_map[img1_name])])
            all_rgb_data.append(pkl_map[int(rgb_map[img2_name])])
            if label == 1:
                test_intra.append([index, index + 1])
            elif label == 0:
                test_extra.append([index, index + 1])
            index += 2
        else:
            continue
    return test_intra, test_extra, all_rgb_data

# train_folder = 'E:/soft/Project/zte/ztedata/youtube/result_folder/'
# test_folder = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_result_folder/'
#
# train_vector, train_label = get_train_data(train_folder)
# # print train_label.__len__()
#
# zte_datalist_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/datalist.txt'
# zte_rgb_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file.csv'
#
# test_vector, test_label = get_zte_test(zte_datalist_path, zte_rgb_path, test_folder)
# print np.array(test_vector).shape
# print np.array(test_label).shape

# a = [1, 2, 3]
# b = [2, 5, 8]
#
# c = np.hstack([a,b])
# c = np.hstack((c,b))
# print c
