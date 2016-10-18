# coding=utf8
# author = 'Aaron Chou'
import sys

import json

reload(sys)
sys.setdefaultencoding('utf-8')

in_file = '/home/aaron/PycharmProjects/myproject1/data/yibao/word2vec//kc25k2_oneline_cut_scatter.txt'
out_file = '/home/aaron/PycharmProjects/myproject1/data/yibao/word2vec//scatter.txt'
data = []
with open(in_file) as f:
    for line in f:
        line = line.strip('\n').split('\t')
        each = [1.0, -0.0, 2, 'UNK']
        each[0] = line[1]
        each[1] = line[2]
        each[3] = line[0]
        data.append(each)
        # break

with open(out_file, 'w') as out:
    out.write(json.dumps(data, ensure_ascii=False))