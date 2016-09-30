# coding=utf8
# author = 'Aaron Chou'
import sys

import MySQLdb
import chardet
import jieba
import jieba.posseg as pseg
import jieba.analyse

import Deep_learning.NLP.participle.thulac as thulac

reload(sys)
sys.setdefaultencoding('utf-8')


def mysql_query(sql):
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='t_weibo')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# thu = thulac.thulac("-model_dir ../../../../data/NLP/participle/thulac/models -seg_only")
sql = "select * from weibo_train_data w where substr(w.time,1,10) = '2015-02-02'"
rows = mysql_query(sql)

contents = ''
for row in rows:
    j = ""
    id = str(row["id"])
    content = row["content"].replace('\n', ' ').replace('\r', ' ')
    content = content.split("http:")
    contents += content[0] + '\n'
    # url = ''
    # if content.__len__() > 1:
    #     url = "http:" + content[1]
    # jieba = pseg.cut(text)
    # for w in jieba:
    #     j += w.word + " "
    #
    # # str = jieba.cut(row["content"])
    # # print (" ".join(str))
    # print id

topK = 20
tags = jieba.analyse.extract_tags(contents, topK=topK, withWeight=True, allowPOS=())
tags1 = jieba.analyse.textrank(contents, topK=topK, withWeight=True)

for each in tags:
    print each[0] + " " + str(each[1])

print
for each in tags1:
    print each[0] + " " + str(each[1])


