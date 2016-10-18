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
        text = i[1].read()
        rows.append([i[0],text])
    cursor.close()
    conn.close()
    return rows


# sql = "select ykc101 from kc25k2"
# 'J44.100','I25.103'
disease = "J44.100"
sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 not IN ('"+disease+"') and length(k2.ykc100) >1 and rownum <1005"
rows = oracle_query(sql)

# jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
file_path = "../../../data/yibao/word2vec/ykc100_others1005_cut.txt"
with open(file_path, 'w') as out:
    for disease, each in rows:
        each = each.replace("\n","").replace("\r","").replace("\t","")
        words = pseg.cut(each)
        text = ''
        for w in words:
            text += w.word + ' '
        # print text
        out.write(text+"\n")
        # break
