# coding=utf8
# author = 'Aaron Chou'
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

def mysqlQuery(sql):
    con = MySQLdb.connect(host='192.168.2.249', db='t_weibo', user='root', passwd='admin', port=3306, charset='utf8')
    # cursor =con.cursor()
    cursor = con.cursor(MySQLdb.cursors.DictCursor)
    # sql = sql.decode("utf8")
    cursor.execute(sql)
    row = cursor.fetchall()
    cursor.close()
    con.close()
    return row

sql = "select * from predict"
rows = mysqlQuery(sql)


