# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import re

def get_max_len(file_path = '../../../data/yibao/word2vec//kc25k2_oneline_cut_out.txt'):
    vec_map = dict()
    with open(file_path) as f:
        for line in f:
            word = line.strip("\n").split("\t")[0]
            vec = line.strip("\n").split("\t")[1].split(",")
            vec_map[word] = vec

    return vec_map


vec_map = get_max_len()
print vec_map.__len__()


