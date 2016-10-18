# coding=utf8
# author = 'Aaron Chou'
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

file_path = '/home/aaron/PycharmProjects/myproject1//data/yibao/word2vec/ykc100_cut_top10.txt'
with open(file_path) as f:
    max = 0
    text = ''
    for line in f:
        len = line.split(" ").__len__()
        if max < len:
            max = len
            text = line
        if len > 20:
            print line
    print max, text


