# coding=utf8
# author = 'AaronChou'
from __future__ import division
from numpy import *
import matplotlib.pyplot as plt
import time
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def mysqlQuery(sql):
    """

    :rtype : MySQL查询
    """
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='o2o')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def excuteSql(sql):
    """

    :rtype : MySQL执行
    """
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='o2o', charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def insert_mysql(t):
    conn = MySQLdb.connect(host='192.168.2.249', user='root', passwd='admin', db='o2o')
    cursor = conn.cursor()
    sql1 = "insert into off_um_rate values(%s,%s,%s,%s)"
    for each in t:
        # sql = "insert into tianchi_mobile_recommendation_predict2 values('"+str(each[0])+"','"+str(each[1])+"','"+str(each[2])+"')"
        cursor.execute(sql1, each)
    conn.commit()
    cursor.close()
    conn.close()


def main():
    # out = open("E:\\Datamining\\tianchi\\o2o\\off_um_rate.txt", "w")
    sql = "SELECT user_id as user_id,merchant_id as merchant_id, tag,COUNT(*) AS num FROM off_t1 o GROUP BY o.user_id,merchant_id,o.tag order by user_id"
    rows = mysqlQuery(sql)
    maps, result = {}, []
    for row in rows:
        key = row["user_id"] + "_" + row["merchant_id"]
        if maps.has_key(key):
            maps[key][row["tag"]] += row["num"]
        else:
            maps[key] = [0, 0, 0]
            maps[key][row["tag"]] += row["num"]

    for ma in maps:
        m = maps[ma]
        sum = m[0] + m[1]
        record_num = m[0] + m[1] + m[2]
        rate = 0.5
        if sum != 0:
            rate = round(m[1] / sum, 5)
        u_id = ma.split("_")[0]
        m_id = ma.split("_")[1]
        result.append([u_id, m_id, rate, sum, record_num])
        # out.write(ma + "," + str(rate) + "," + str(sum) + "," + str(record_num) + "\n")
    # out.close()
    print "Insert Mysql..."
    excuteSql("TRUNCATE TABLE off_um_rate")
    insert_mysql(result)

main()