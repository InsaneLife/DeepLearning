# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('../../../../data/NLP/sougou/news_oneline.txt')
read = f.readlines()
f.close()

f = open('../../../../data/NLP/sougou/news_oneline_cut.txt', 'w')
for each in read:
    each = each.split(" ")
    for i in range(2000000):
        f.write(each[i]+' ')
f.close()



