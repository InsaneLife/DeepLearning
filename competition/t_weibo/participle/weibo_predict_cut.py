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
sql = "select id,content from weibo_predict_data"
rows = mysql_query(sql)
with open('../../../../data/competition/t_weibo/participle_predict_jieba.csv', 'w') as out:
    for row in rows:
        j = ""
        id = str(row["id"])
        content = row["content"].replace('\n',' ').replace('\r',' ')
        content = content.split("http:")
        text = content[0]
        url = ''
        if content.__len__() > 1:
            url = "http:" + content[1]
        jieba = pseg.cut(text)
        for w in jieba:
            j += w.word + " "

        # str = jieba.cut(row["content"])
        # print (" ".join(str))
        out.write(id+",,,"+j + url + '\n')
        print id
        #break
