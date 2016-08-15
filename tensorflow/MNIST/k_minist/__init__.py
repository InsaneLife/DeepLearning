# coding=utf8
# author = 'Aaron Chou'
import sys
import numpy as np
import numpy
from numpy import *
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('data/train.csv')
train = f.readlines()
f.close()

f = open('data/test.csv')
test = f.readlines()
f.close()
i = 0
print test.__len__()
for each in test:
    print each
    break