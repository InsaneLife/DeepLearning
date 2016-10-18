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
sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 IN ( 'J44.100','I25.103','J20.900','E11.900','H25.900','I67.803','M51.202','I10.x05','I10.x00','N20.100') and length(k2.ykc100) >1"
rows = oracle_query(sql)

# jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
file_path = '../../../../data/yibao/word2vec/ykc100_cut_top10.txt'
with open(file_path, 'w') as out:
    for disease, each in rows:
        each = each.replace("\n","").replace("\r","").replace("\t","")
        words = pseg.cut(each)
        text = ''
        for w in words:
            if w.flag != 'x':
                text += w.word + ' '
        # print text
        out.write(disease + ',' +text+"\n")
        # break
