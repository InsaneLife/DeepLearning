# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import Deep_learning.NLP.participle.thulac as thulac

thu = thulac.thulac("-model_dir ../../../data/NLP/participle/thulac/models")
str = "习近平访问了美国"
ss = " ".join(thu.cut(str))
print ss


