# coding=utf8
# author = 'Aaron Chou'
import re
import sys
import chardet
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')

with open('../../../data/NLP/sougou/result/news_oneline_cut_out.txt') as f:
    read = f.readlines(10)
    for each in read:
        print each.strip()
