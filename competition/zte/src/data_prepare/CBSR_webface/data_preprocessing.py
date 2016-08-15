# coding=utf-8
# author = 'AaronChou'

import random
import sys
import os
import numpy as np
import numpy
from PIL import Image


class DataSet(object):
    def __init__(self, images, labels, fake_data=False):
        if fake_data:
            self._num_examples = 10000
        else:
            assert images.shape[0] == labels.shape[0], (
                "images.shape: %s labels.shape: %s" % (images.shape,
                                                       labels.shape))
            self._num_examples = images.shape[0]
            # Convert shape from [num examples, rows, columns, depth]
            # to [num examples, rows*columns] (assuming depth == 1)
            # if len(images.shape) == 3:
            assert images.shape[3] == 1
            images = images.reshape(images.shape[0], images.shape[1] * images.shape[2])
            # Convert from [0, 255] -> [0.0, 1.0].
            images = images.astype(numpy.float32)
            images = numpy.multiply(images, 1.0 / 255.0)
        self._images = images
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size, fake_data=False):
        """Return the next `batch_size` examples from this data set."""
        if fake_data:
            fake_image = [1.0 for _ in xrange(784)]
            fake_label = 0
            return [fake_image for _ in xrange(batch_size)], [
                fake_label for _ in xrange(batch_size)]
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]


def walk_through_folder_for_split(src_folder):
    test_set, train_set, validate_set = [], [], []
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
        interval = (people_imgs.__len__() - 1) / 5
        test_set += people_imgs[0:interval]
        validate_set += people_imgs[interval:interval * 2]
        train_set += people_imgs[interval * 2:]

        sys.stdout.write('\rdone: ' + str(label))
        sys.stdout.flush()
        label += 1
    print ''
    print 'test  set num: %d' % (len(test_set))
    print 'train set num: %d' % (len(train_set))
    print 'validate set num: %d' % (len(validate_set))
    random.shuffle(test_set)
    random.shuffle(train_set)
    random.shuffle(validate_set)
    return test_set, train_set, validate_set


def cPickle_output(vars, file_name):
    import cPickle

    f = open(file_name, 'wb')
    cPickle.dump(vars, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def vectorize_imgs_and_save(path_and_labels, image_size, vector_folder, batch_size=1000):
    if not vector_folder.endswith('/'):
        vector_folder += '/'
    if not os.path.exists(vector_folder):
        os.mkdir(vector_folder)

    arrs, labels = [], []
    i = 0
    batch_index = 0
    for path_and_label in path_and_labels:
        path, label = path_and_label
        im = Image.open(path)
        if im.mode != 'RGB':
            continue
        # cut and resize im
        x_size, y_size = im.size
        start_point_xy = x_size / 5
        end_point_xy = x_size / 5 + x_size * 3 / 5
        box = (start_point_xy, start_point_xy, end_point_xy, end_point_xy)
        img = im.crop(box)
        img = img.resize(image_size)

        arr_img = np.asarray(img, dtype='float32')
        arr_img = rgb2gray(arr_img)
        # arr_img = arr_img.reshape(arr_img.shape[0] * arr_img.shape[1])
        # arr_img = np.multiply(arr_img, 1.0 / 255.0)

        labels.append(label)
        arrs.append(arr_img)
        if arrs.__len__() == batch_size:
            arrs = np.asarray(arrs, dtype='float32')
            labels = np.asarray(labels, dtype='int32')
            file_name = vector_folder + str(batch_index) + '.pkl'
            cPickle_output((arrs, labels), file_name)
            batch_index += 1
            arrs = []
            labels = []
        i += 1
        if i % 100 == 0:
            sys.stdout.write('\rdone: ' + str(i))
            sys.stdout.flush()
    print ''
    arrs = np.asarray(arrs, dtype='float32')
    labels = np.asarray(labels, dtype='int32')
    file_name = vector_folder + str(batch_index) + '.pkl'
    cPickle_output((arrs, labels), file_name)


def vectorize_imgs(path_and_labels, image_size, batch_size=1000):
    arrs, labels = [], []
    i = 0
    batch_index = 0
    for path_and_label in path_and_labels:
        path, label = path_and_label
        im = Image.open(path)
        if im.mode != 'RGB':
            continue
        # cut and resize im
        x_size, y_size = im.size
        start_point_xy = x_size / 5
        end_point_xy = x_size / 5 + x_size * 3 / 5
        box = (start_point_xy, start_point_xy, end_point_xy, end_point_xy)
        img = im.crop(box)
        img = img.resize(image_size)

        arr_img = np.asarray(img, dtype='float32')
        arr_img = rgb2gray(arr_img)
        # arr_img = arr_img.reshape(arr_img.shape[0] * arr_img.shape[1])
        # arr_img = np.multiply(arr_img, 1.0 / 255.0)

        labels.append(label)
        arrs.append(arr_img)
        i += 1
        if i % 100 == 0:
            sys.stdout.write('\rdone: ' + str(i))
            sys.stdout.flush()
    print ''
    arrs = np.asarray(arrs, dtype='float32')
    labels = np.asarray(labels, dtype='int32')
    return arrs, labels


def save_vectorize_imgs(src_folder='../../../data/csia/CASIA-WebFace/',
                        test_vector_folder='../../../data/csia/test_vector1/',
                        train_vector_folder='../../../data/csia/train_vector/',
                        validate_vector_folder='../../../data/csia/train_vector/'):
    # split train and test, test_set [imgpath,label]
    test_path_labels, train_path_labels, validate_path_labels = walk_through_folder_for_split(src_folder)

    img_size = (50, 50)  # not used
    vectorize_imgs_and_save(test_path_labels, img_size, test_vector_folder)
    vectorize_imgs_and_save(train_path_labels, img_size, train_vector_folder)
    vectorize_imgs_and_save(validate_path_labels, img_size, validate_vector_folder)


def read_pkl(folder):
    files = os.listdir(folder)
    data = []
    for file in files:
        print file
    return data

def read_data_sets(test_vector_folder='../../../data/csia/test_vector1/',
                   train_vector_folder='../../../data/csia/train_vector/',
                   validate_vector_folder='../../../data/csia/train_vector/'):
    class DataSets(object):
        pass
    data_sets = DataSets()
    train_images = read_pkl(train_vector_folder)
    return data_sets


save_vectorize_imgs()
