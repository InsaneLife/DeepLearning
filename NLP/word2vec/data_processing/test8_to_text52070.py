# coding=utf8
# author = 'Aaron Chou'
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')


def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words"""
    with zipfile.ZipFile(filename) as f:
        data = f.read(f.namelist()[0])
    return data

filename = '../../../../data//word2vec/test8.zip'
data = read_data(filename)
print
