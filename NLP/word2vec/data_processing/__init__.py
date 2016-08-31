# coding=utf8
# author = 'Aaron Chou'
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

# filename = '../../../..//data/NLP/sougou/news_oneline.txt'
# with open(filename) as f:
#      data = f.readline().decode('utf-8')
#
#
# filename = '../../../../data/word2vec/text8.zip'
# with zipfile.ZipFile(filename) as f:
#     data = f.read(f.namelist()[0])
#
#     print 'yes'
#
# # Read the data into a list of strings.
# def read_data(filename):
#     """Extract the first file enclosed in a zip file as a list of words"""
#     with zipfile.ZipFile(filename) as f:
#         data = f.read(f.namelist()[0])
#     return data

s = "公安机关销毁１０余万非法枪支　跨国武"
s = s.replace('　','')
print s