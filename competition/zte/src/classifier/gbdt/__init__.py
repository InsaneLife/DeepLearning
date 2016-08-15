__author__ = 'Bean'
# coding=utf8
import cPickle
from numpy import array
import numpy as np
from PIL import Image

path = 'E:/soft/Project/zte/ztedata/youtube/result_folder/0.pkl'


def get_traindata(path):
    f = open(path, 'rb')
    vector, label = cPickle.load(f)
    f.close()
    for i in range(0, len(vector)):
        print vector[i], label[i]
        break


data = [[5, 8], [5, 9]]
data = np.array(data)
print np.sum(data, 1)
print data.shape[1]
print np.repeat(np.sum(data, 1), data.shape[1])
print np.repeat(np.sum(data, 1), data.shape[1]).reshape(data.shape[0], data.shape[1])
data = np.divide(data, np.repeat(np.sum(data, 1), data.shape[1]).reshape(data.shape[0], data.shape[1]))

print data
