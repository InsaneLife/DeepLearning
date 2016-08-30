# coding=utf8
# author = 'Aaron Chou'
import re
import sys
import chardet
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np

import matplotlib

matplotlib.use('Agg')

from matplotlib.pyplot import plot, savefig

x = np.linspace(-4, 4, 30)
y = np.sin(x);

plot(x, y, '--*b')

savefig('MyFig.jpg')



