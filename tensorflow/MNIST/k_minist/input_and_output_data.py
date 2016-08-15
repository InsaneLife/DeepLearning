# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Functions for downloading and reading MNIST data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import gzip
import os
import numpy
from numpy import *


def _read32(bytestream):
    dt = numpy.dtype(numpy.uint32).newbyteorder('>')
    return numpy.frombuffer(bytestream.read(4), dtype=dt)


def extract_images(filename = 'data/train.csv'):
    """Extract the images into a 4D uint8 numpy array [index, y, x, depth]."""
    train_images, train_labels, test_images, test_labels = [], [], [], []
    with open(filename) as f:
        train_file = f.readlines()
    i = 0
    interval = (train_file.__len__() - 1)/5
    for each_line in train_file:
        if each_line[0] == 'l':
            continue
        each_line = each_line.strip('\n')
        eachs = each_line.split(',')
        label = zeros(10)
        label[int(eachs[0])] = 1
        if i < interval:
            test_images.append(eachs[1:])
            test_labels.append(label)
        else:
            train_images.append(eachs[1:])
            train_labels.append(label)
        i += 1
    train_images = numpy.array(train_images)
    train_labels = numpy.array(train_labels)
    test_images = numpy.array(test_images)
    test_labels = numpy.array(test_labels)
    return train_images, train_labels,  test_images, test_labels


def dense_to_one_hot(labels_dense, num_classes=10):
    """Convert class labels from scalars to one-hot vectors."""
    num_labels = labels_dense.shape[0]
    index_offset = numpy.arange(num_labels) * num_classes
    labels_one_hot = numpy.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot



def extract_labels(filename, one_hot=False):
    """Extract the labels into a 1D uint8 numpy array [index]."""
    print('Extracting', filename)
    with gzip.open(filename) as bytestream:
        magic = _read32(bytestream)
        if magic != 2049:
            raise ValueError(
                'Invalid magic number %d in MNIST label file: %s' %
                (magic, filename))
        num_items = _read32(bytestream)
        buf = bytestream.read(num_items)
        labels = numpy.frombuffer(buf, dtype=numpy.uint8)
        if one_hot:
            return dense_to_one_hot(labels)
        return labels


class DataSet(object):
    def __init__(self, images, labels, fake_data=False):
        if fake_data:
            self._num_examples = 10000
        else:
            assert images.shape[0] == labels.shape[0], (
                "images.shape: %s labels.shape: %s" % (images.shape,
                                                       labels.shape))
            self._num_examples = images.shape[0]

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


def read_data_sets(local_file = "data/train.csv", k_testfile = "data/test.csv", fake_data=False, one_hot=False):
    class DataSets(object):
        pass

    data_sets = DataSets()
    if fake_data:
        data_sets.train = DataSet([], [], fake_data=True)
        data_sets.validation = DataSet([], [], fake_data=True)
        data_sets.test = DataSet([], [], fake_data=True)
        data_sets.k_test = DataSet([], [], fake_data=True)
        return data_sets
    VALIDATION_SIZE = 5000


    train_images, train_labels,  test_images, test_labels = extract_images(local_file)
    validation_images = train_images[:VALIDATION_SIZE]
    validation_labels = train_labels[:VALIDATION_SIZE]
    train_images = train_images[VALIDATION_SIZE:]
    train_labels = train_labels[VALIDATION_SIZE:]
    data_sets.train = DataSet(train_images, train_labels)
    data_sets.validation = DataSet(validation_images, validation_labels)
    data_sets.test = DataSet(test_images, test_labels)

    k_test_data, k_test_labels = get_kaggle_test(k_testfile)
    data_sets.k_test = DataSet(k_test_data, k_test_labels)
    return data_sets

def get_kaggle_test(file_path, fake_data=False):
    test_data, test_labels = [], []
    with open(file_path) as f:
        test_file = f.readlines()

    for each in test_file:
        if each[0] == 'p':
            continue
        each = each.strip('\n')
        eachs = each.split(',')
        test_data.append(eachs)

        label = zeros(10)
        label[1] = 1
        test_labels.append(label)
    test_data = numpy.array(test_data)
    test_labels = numpy.array(test_labels)
    return test_data, test_labels

def output_result(result):

    out = open('data/submit.csv')
    out.write('ImageId,Label\n')
    i = 0
    for each in result:
        out.write(str(i) + ',' + str(each) + '\n')
        i += 1
    out.close()



