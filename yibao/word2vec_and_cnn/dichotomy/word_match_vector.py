# coding=utf8
# author = 'Aaron Chou'
import sys

import chardet
import cx_Oracle as cx_Oracle
import jieba.posseg as pseg
import jieba
import numpy as np

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
        rows.append([i[0], text])
    cursor.close()
    conn.close()
    return rows


def get_word_vector(path="../../../../data/yibao/panzhihua/word2vec/kc25k2_word2vec_cbow.txt"):
    word_vector_map = {}
    with open(path) as f:
        for line in f:
            # UNK	0.138251,-0.0511282,0.134034,-0.00142783...
            word = line.strip("\n").split("\t")[0]
            vector = line.strip("\n").split("\t")[1].split(",")
            word_vector_map[word] = vector
    return word_vector_map


def get_n_ecample(disease="J44.100", word_vector_map=dict()):
    # sql = "select ykc101 from kc25k2"
    sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 not IN ('" + disease + "') and length(k2.ykc100) >1 and rownum <1005"
    rows = oracle_query(sql)

    train_vectors, train_labels = [], []
    # jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
    for disease, each in rows:
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        vectors = np.zeros(4096)
        i = 0
        for w in words:
            if w.flag != 'x':
                for v in word_vector_map[w.word.encode("utf8")]:
                    vectors[i] = float(v)
                    i += 1
        train_vectors.append(vectors)
        train_labels.append([1, 0])
    return train_vectors, train_labels


def get_p_ecample(disease="J44.100", word_vector_map={}):
    # sql = "select ykc101 from kc25k2"
    sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 in ('" + disease + "') and length(k2.ykc100) >1"
    rows = oracle_query(sql)

    train_vectors, train_labels = [], []
    # jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
    for disease, each in rows:
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        vectors = np.zeros(4096)
        i = 0
        for w in words:
            if w.flag != 'x':

                for v in word_vector_map[w.word.encode("utf8")]:
                    vectors[i] = float(v)
                    i += 1
        train_vectors.append(vectors)
        train_labels.append([0, 1])
    return train_vectors, train_labels


def get_data():
    word_vector_map = get_word_vector()
    data_n_vectors, data_n_labels = get_n_ecample(disease="J44.100", word_vector_map=word_vector_map)
    data_p_vectors, data_p_labels = get_p_ecample(disease="J44.100", word_vector_map=word_vector_map)
    interval = int(data_n_labels.__len__() / 5)

    train_vectors = np.concatenate((data_n_vectors[interval:], data_p_vectors[interval:]))
    train_labels = np.concatenate((data_n_labels[interval:], data_p_labels[interval:]))

    test_vectors = np.concatenate((data_n_vectors[:interval], data_p_vectors[:interval]))
    test_labels = np.concatenate((data_n_labels[:interval], data_p_labels[:interval]))

    return train_vectors, train_labels, test_vectors, test_labels

def get_gbdt_data():
        word_vector_map = get_word_vector()
        data_n_vectors, data_n_labels = get_n_ecample(disease="J44.100", word_vector_map=word_vector_map)
        data_p_vectors, data_p_labels = get_p_ecample(disease="J44.100", word_vector_map=word_vector_map)
        len = data_n_labels.__len__()
        data_n_labels = [0 for i in range(len)]
        data_p_labels = [1 for i in range(data_p_vectors.__len__())]

        interval = int(len / 5)

        train_vectors = np.concatenate((data_n_vectors[interval:], data_p_vectors[interval:]))
        train_labels = np.concatenate((data_n_labels[interval:], data_p_labels[interval:]))

        test_vectors = np.concatenate((data_n_vectors[:interval], data_p_vectors[:interval]))
        test_labels = np.concatenate((data_n_labels[:interval], data_p_labels[:interval]))

        return train_vectors, train_labels, test_vectors, test_labels

        # get_data()