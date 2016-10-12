# coding=utf8
# author = 'Aaron Chou'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import gzip
import os
import numpy


def _read32(bytestream):
    dt = numpy.dtype(numpy.uint32).newbyteorder('>')
    return numpy.frombuffer(bytestream.read(4), dtype=dt)


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
            # Convert shape from [num examples, rows, columns, depth]
            # to [num examples, rows*columns] (assuming depth == 1)
            # if len(images.shape) == 3:
            # assert images.shape[3] == 1
            # images = images.reshape(images.shape[0], images.shape[1] * images.shape[2])
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


def get_sentence_vector(file_path='../../../data/yibao/panzhihua/word2vec_and_cnn/ykc100_cut_vector_top10.txt'):


    word_vectors, labels, disease_map, class_index = [], [], {}, 0
    with open(file_path) as f:
        for line in f:
            # J20.900,咳嗽 10 天
            # transform into one hot
            line = line.replace("]","").replace("[","").replace("\n","")
            data = line.split(",")
            label = numpy.zeros(10)
            label[data[0]] = 1
            vectors = data[1:]
            word_vectors.append(vectors)
            labels.append(label)
    interval = int((labels.__len__() - 1) / 5)
    test_vectors = numpy.array(word_vectors[:interval])
    test_labels = numpy.array(labels[:interval])
    train_vectors = numpy.array(word_vectors[interval:])
    train_labels = numpy.array(labels[interval:])
    return train_vectors, train_labels, test_vectors, test_labels


def read_data_sets(file_path='../../../data/yibao/panzhihua/word2vec_and_cnn/ykc100_cut_vector_top10.txt', fake_data=False, one_hot=False):
    class DataSets(object):
        pass

    data_sets = DataSets()
    if fake_data:
        data_sets.train = DataSet([], [], fake_data=True)
        data_sets.validation = DataSet([], [], fake_data=True)
        data_sets.test = DataSet([], [], fake_data=True)
        data_sets.k_test = DataSet([], [], fake_data=True)
        return data_sets
    VALIDATION_SIZE = 500

    train_images, train_labels, test_images, test_labels = get_sentence_vector(file_path)
    validation_images = train_images[:VALIDATION_SIZE]
    validation_labels = train_labels[:VALIDATION_SIZE]
    train_images = train_images[VALIDATION_SIZE:]
    train_labels = train_labels[VALIDATION_SIZE:]

    data_sets.train = DataSet(train_images, train_labels)
    data_sets.validation = DataSet(validation_images, validation_labels)
    data_sets.test = DataSet(test_images, test_labels)

    return data_sets


# read_data_sets(file_path='../../../data/yibao/panzhihua/word2vec_and_cnn/ykc100_cut_vector_top10.txt')
