# coding=utf8
# author = 'Aaron Chou'
import os
import sys
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')


data_folder = 'data/'
files = os.listdir(data_folder)
for file in files:
    with open(data_folder+file) as f:
        data, label = cPickle.load(f)
    print data.shape


