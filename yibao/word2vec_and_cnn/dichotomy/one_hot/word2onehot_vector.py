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


def generate_word_one_hot_vector(disease="J44.100",dimension=800):
    word_vector_map, word_set = {}, set()
    sql = "SELECT k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 not IN ('" + disease + "') and length(k2.ykc100) >1 and rownum <1005"
    rows = oracle_query(sql)
    for each in rows:
        each = each[0]
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        for w in words:
            if w.flag != 'x':
                word_set.add(w.word.encode("utf8"))

    sql = "SELECT k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 in ('" + disease + "') and length(k2.ykc100) >1"
    rows = oracle_query(sql)
    for each in rows:
        each = each[0]
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        for w in words:
            if w.flag != 'x':
                word_set.add(w.word.encode("utf8"))

    i = 0
    for word in word_set:
        vector = np.zeros(dimension)
        vector[i] = 1
        word_vector_map[word] = vector
        i += 1
    return word_vector_map


def get_n_ecample(disease="J44.100", word_vector_map=dict(), dimension=800):
    # sql = "select ykc101 from kc25k2"
    sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 not IN ('" + disease + "') and length(k2.ykc100) >1 and rownum <1005"
    rows = oracle_query(sql)

    train_vectors, train_labels = [], []
    # jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
    for disease, each in rows:
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        size = dimension*32
        vectors = np.zeros(size)
        i = 0
        for w in words:
            if w.flag != 'x':
                for v in word_vector_map[w.word.encode("utf8")]:
                    if i > size:
                        continue
                    vectors[i] = float(v)
                    i += 1
        train_vectors.append(vectors)
        train_labels.append([1, 0])
    return train_vectors, train_labels


def get_p_ecample(disease="J44.100", word_vector_map={}, dimension=800):
    # sql = "select ykc101 from kc25k2"
    sql = "SELECT k.ykc605,k2.ykc100 FROM kc25 K LEFT JOIN kc25k2 k2 ON k.ykc009=k2.ykc009 where k.ykc605 in ('" + disease + "') and length(k2.ykc100) >1"
    rows = oracle_query(sql)

    train_vectors, train_labels = [], []
    # jieba.load_userdict("../../../data/NLP/participle/lexicon/ciku.txt")
    for disease, each in rows:
        each = each.replace("\n", "").replace("\r", "").replace("\t", "")
        words = pseg.cut(each)
        size = dimension * 32
        vectors = np.zeros(size)
        i = 0
        for w in words:
            if w.flag != 'x':
                for v in word_vector_map[w.word.encode("utf8")]:
                    if i > size:
                        continue
                    vectors[i] = float(v)
                    i += 1
        train_vectors.append(vectors)
        train_labels.append([0, 1])
    return train_vectors, train_labels


def get_data():
    word_vector_map = generate_word_one_hot_vector(disease="J44.100", dimension=800)
    data_n_vectors, data_n_labels = get_n_ecample(disease="J44.100", word_vector_map=word_vector_map, dimension=800)
    data_p_vectors, data_p_labels = get_p_ecample(disease="J44.100", word_vector_map=word_vector_map, dimension=800)
    interval = int(data_n_labels.__len__() / 5)

    train_vectors = np.concatenate((data_n_vectors[interval:], data_p_vectors[interval:]))
    train_labels = np.concatenate((data_n_labels[interval:], data_p_labels[interval:]))

    test_vectors = np.concatenate((data_n_vectors[:interval], data_p_vectors[:interval]))
    test_labels = np.concatenate((data_n_labels[:interval], data_p_labels[:interval]))

    return train_vectors, train_labels, test_vectors, test_labels

def get_gbdt_data():
    word_vector_map = generate_word_one_hot_vector(disease="J44.100")
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

