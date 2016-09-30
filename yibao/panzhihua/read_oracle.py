# coding=utf8
# author = 'Aaron Chou'
import sys

import chardet
import cx_Oracle as cx_Oracle
import jieba.posseg as pseg
reload(sys)
sys.setdefaultencoding('utf-8')
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def oracle_query(sql, url='CSI_PZH/123456@192.168.2.98:1521/orcl'):
    # conn = cx_Oracle.connect("CSI_PZH", "123456", "192.168.2.98:1521/orcl")
    conn = cx_Oracle.connect(url)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def oracle_query_clob(sql, url='CSI_PZH/123456@192.168.2.98:1521/orcl'):
    # conn = cx_Oracle.connect("CSI_PZH", "123456", "192.168.2.98:1521/orcl")
    conn = cx_Oracle.connect(url)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = []
    for i in cursor:
        text = i[0].read()
        rows.append(text)
    cursor.close()
    conn.close()
    return rows


sql = "select ykc101 from kc25k2"
rows = oracle_query_clob(sql)
file_path = '/home/aaron/PycharmProjects/myproject1/data/yibao/panzhihua/oneline_cut.txt'
with open(file_path, 'w') as out:
    for each in rows:
        words = pseg.cut(each)
        text = ''
        for w in words:
            if w.flag != 'x':
                text += w.word + ' '
        # print text
        out.write(text)
        # break
