# coding=utf8
# author = 'Aaron Chou'
import re
import sys
import chardet
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('../../data/NLP/sougou/news_tensite_xml.smarty.dat', 'r')
read = f.readlines()
f.close()

out = open('../../data/NLP/sougou/news_out.txt', 'w')
for each in read:
    # print chardet.detect(each)
    each = each.strip().decode('GB2312', 'ignore')
    each = re.sub('<.*?>', '', each)
    word_list = jieba.cut(each)
    word_list = " ".join(word_list)
    out.write(word_list.encode('utf-8')+'\n')
    print each



out.close()



