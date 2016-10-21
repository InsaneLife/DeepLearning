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


def get_test():
    sql = "select * from offline_test"
    rows = mysqlQuery(sql)
    return rows

def get_user_rate():
    sql = "select * from off_u_rate order by user_id"
    rows = mysqlQuery(sql)
    maps = {}
    for row in rows:
        if maps.has_key(row["user_id"]):
            maps[row["user_id"]][row["tag"]] += row["num"]
        else:
            maps[row["user_id"]] = [0, 0, 0]
            maps[row["user_id"]][row["tag"]] += row["num"]

    user_rate = {}
    for ma in maps:
        m = maps[ma]
        sum = m[0]+m[1]
        rate = 0.5
        if sum != 0:
            rate = round(m[1] / sum,5)
        user_rate[ma] = rate
    return user_rate

def main():
    out = open("E:\\Datamining\\tianchi\\o2o\\submit.csv", "w")
    user_rate = get_user_rate()
    test_rows = get_test()
    for row in test_rows:
        if user_rate.has_key(row["User_id"]):
            out.write(str(row["User_id"])+","+str(row["Coupon_id"])+","+str(row["Date_received"])+","+ str(user_rate[row["User_id"]])+"\n")
        else:
            out.write(str(row["User_id"])+","+str(row["Coupon_id"])+","+str(row["Date_received"])+","+ str(0.5)+"\n")
    out.close()

main()