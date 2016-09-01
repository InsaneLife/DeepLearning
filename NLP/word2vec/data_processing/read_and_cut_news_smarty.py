# coding=utf8
# author = 'Aaron Chou'
import re
import sys
import chardet
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')

f = open('../../../../data/NLP/sougou/news_tensite_xml.smarty.dat', 'r')
read = f.readlines()
f.close()

i = 0
out = open('../../../../data/NLP/sougou/news_oneline_smarty.txt', 'w')
for each in read:
    # print chardet.detect(each)
    each = each.strip().decode('GB2312', 'ignore')
    each = re.sub('<.*?>', '', each)
    if each.__len__() == 0:
        continue
    if each[0] == 'h':
        i = 0
    if i == 2 or i == 3:
        # punctuation filter
        each = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), each)
        each = each.replace(' ', '').replace('\t', '').replace('　', '')
        word_list = jieba.cut(each)
        word_list = " ".join(word_list)
        out.write(word_list.encode('utf-8') + " ")
    i += 1

out.close()
