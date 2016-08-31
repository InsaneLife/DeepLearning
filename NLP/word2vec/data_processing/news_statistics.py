# coding=utf8
# author = 'Aaron Chou'
import re
import sys
import chardet
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('../../../../data/NLP/sougou/news_tensite_xml.dat', 'r')
read = f.readlines()
f.close()

i = 0
for each in read:
    # print chardet.detect(each)
    each = each.strip().decode('GB2312', 'ignore')
    each = re.sub('<.*?>', '', each)
    if each.__len__() == 0:
        continue
    if each[0] == 'h':
        i += 1
print i





