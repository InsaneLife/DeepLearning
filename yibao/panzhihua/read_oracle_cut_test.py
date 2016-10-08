# coding=utf8
# author = 'Aaron Chou'
import sys

import chardet
import cx_Oracle as cx_Oracle
import jieba.posseg as pseg
import jieba

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


sql = "select ykc101 from kc25k2 where rownum<100"
rows = oracle_query_clob(sql)

jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
file_path = '/home/aaron/PycharmProjects/myproject1/data/yibao/panzhihua/word_cut_ciku.txt'
with open(file_path, 'w') as out:
    for each in rows:
        each = each.replace("\n","").replace("\r","").replace("\t","")
        words = jieba.cut(each)
        text = ''
        for w in words:
            text += w + ' '
        # print text
        out.write(text+"\n")
        # break
