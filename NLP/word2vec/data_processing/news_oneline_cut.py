# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('../../../../data/NLP/sougou/news_oneline.txt')
read = f.readlines()
f.close()

f = open('../../../../data/NLP/sougou/news_oneline_cut.txt', 'w')
val = open('../../../../data/NLP/sougou/news_oneline_validation.txt', 'w')
cut_size = 2000000
validation_size = 50000

for each in read:
    each = each.split(" ")
    for i in range(cut_size):
        f.write(each[i]+' ')
    for i in range(cut_size,cut_size + validation_size):
        val.write(each[i]+' ')
f.close()
val.close()


