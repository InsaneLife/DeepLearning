# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from textblob import TextBlob

wiki = TextBlob("Python is a high-level, general-purpose programming language.")
print wiki.tags



