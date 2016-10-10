# coding=utf8
# author = 'AaronChou'
import cx_Oracle
from numpy import *
import matplotlib.pyplot as plt
import time
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def excuteSql(sql):
    """

    :rtype : MySQL执行
    """
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='t_lastmile', charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def excuteInsertManySql(sql, list):
    """

    :rtype : MySQL Insert
    """
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='t_lastmile', charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.executemany(sql, list)
    conn.commit()
    cursor.close()
    conn.close()


def mysqlQuery(sql):
    """

    :rtype : MySQL查询
    """
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='t_lastmile')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def oracleQuery(sql):
    # dsnStr = cx_Oracle.makedsn("192.168.3.134", "1521", "scxnh4")
    # conn = cx_Oracle.connect(user="NH_SCTEST", password="NH_SCTEST123", dsn=dsnStr)
    conn = cx_Oracle.connect( 'NH_SCTEST', 'NH_SCTEST123','192.168.3.134:1521:scxnh4')
    #connection by service_name: user/pass@hostname:port/SERVICE_NAME
    #connection by sid user/pass@hostname:port:SID -- NOTE the colon!
    #conn= cx_Oracle.connect(host='192.168.2.134',db='scxnh4',user='NH_SCTEST',passwd='NH_SCTEST123',port=1521,charset='utf8')

    #conn = cx_Oracle.connect('xnh/123456@192.168.2.133:1521/XE')
    #conn = cx_Oracle.connect( "NHDBA", "xnh123456","192.168.2.134:1521/orcl")
    cursor = conn.cursor ()
    #sql = sql.decode("utf8")
    #print sql
    cursor.execute (sql)
    row = cursor.fetchall ()
    cursor.close()
    conn.close()
    return row
