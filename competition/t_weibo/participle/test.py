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


thu = thulac.thulac("-model_dir ../../../../data/NLP/participle/thulac/models_pro -seg_only")
sql = "select id,content from weibo_train_data"
rows = mysql_query(sql)

for row in rows:

    id = row["id"]
    content = row["content"].replace('\n', ' ').replace('\r', ' ')
    seg = " ".join(thu.cut(content))

    str = jieba.cut(row["content"])
    print (" ".join(str))
    print seg
    if id == 10:
        break

