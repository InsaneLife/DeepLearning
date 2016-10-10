# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import re

def get_max_len(file_path = '/home/aaron/PycharmProjects/myproject1/data/yibao/panzhihua/word_cut.txt'):
    max = 0
    with open(file_path) as f:
        for line in f:
            length = line.split(" ").__len__()
            if length > max:
                max = length

    print length
    return length

get_max_len()

string = "asdsa，"
string = re.sub(r"，", "", string)
print string

