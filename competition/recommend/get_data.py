# coding=utf8
import cPickle
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing

import MySQLdb
import sys
from sklearn import ensemble

reload(sys)
sys.setdefaultencoding('utf-8')


def excuteSql(sql):
    """

    :rtype : MySQL执行
    """
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='tianchi', charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def get_train():
    # sql = "select * from tianchi_r_10 r "
    sql = "select r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg,max(nextgs) as nextgs,rankul from tianchi_r_10 r GROUP BY r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg, rankul"
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    train_x = []
    train_y = []
    for each in row:
        train_x.append([int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                        int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        train_y.append(int(each["nextgs"]))
    cursor.close()
    conn.close()
    # return mat(train_x), mat(train_y).transpose()
    return train_x, train_y

def split_train():
    VALIDATION_SIZE = 5000
    x, y = get_train()
    scaler = preprocessing.StandardScaler().fit(x)
    x = scaler.transform(x)
    len = x.__len__()
    split_num = len/10
    train_x = np.array(x[split_num + VALIDATION_SIZE:])
    train_y = np.array(y[split_num + VALIDATION_SIZE:])
    validation_x = np.array(x[split_num:split_num + VALIDATION_SIZE])
    validation_y = np.array(y[split_num:split_num + VALIDATION_SIZE])
    test_x = np.array(x[:split_num])
    test_y = np.array(y[:split_num])
    return train_x, train_y, validation_x, validation_y, test_x, test_y, scaler

def get_test_1217():
    # sql = "select * from tianchi_r_10 r "
    sql = "select r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg,nextgs,rankul from test_1217 r"
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    train_x = []
    train_y = []
    for each in row:
        train_x.append([int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                        int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        train_y.append(int(each["nextgs"]))
    cursor.close()
    conn.close()
    # return mat(train_x), mat(train_y).transpose()
    return np.array(train_x), np.array(train_y)


def getForcast():
    sql = "SELECT * FROM tianchi_fresh_test8 t "
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    test_x = []
    x = []
    for each in row:
        test_x.append([int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                       int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        x.append([each["user_id"], each["item_id"]])
    cursor.close()
    conn.close()
    # return mat(test_x), x
    return np.array(test_x), np.array(x)


def insertMysql(t):
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor()
    sql1 = "insert into tianchi_predict4 values(%s,%s,%s)"
    for each in t:
        # sql = "insert into tianchi_mobile_recommendation_predict2 values('"+str(each[0])+"','"+str(each[1])+"','"+str(each[2])+"')"
        cursor.execute(sql1, each)
    conn.commit()
    cursor.close()
    conn.close()


train_x, train_y, validation_x, validation_y, test_x, test_y = split_train()
print train_x.shape, train_y.shape