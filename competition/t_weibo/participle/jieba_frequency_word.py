# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import jieba
import jieba.analyse
from optparse import OptionParser



file_name = '../../../../data/competition/t_weibo/participle_predict_jieba.csv'

topK = 10


content = open(file_name, 'rb').read()

tags = jieba.analyse.extract_tags(content, topK=topK)

print("\n".join(tags))



