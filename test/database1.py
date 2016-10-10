# -*- coding: utf-8 -*-
from time import sleep

import urllib2
import json
import MySQLdb
import simplejson as simplejson
import cx_Oracle
import MySQLdb
import cx_Oracle




def updateFrequency(map):
    conn = cx_Oracle.connect( "xnh", "123456","192.168.2.133:1521/XE")
    #conn = cx_Oracle.connect('xnh/123456@192.168.2.133:1521:XE')
    i=0
    cursor = conn.cursor ()
    for id in map:
        print id
        sqls="UPDATE a SET a.a = '1' WHERE a.b=%s"
        print sqls
        cursor.execute(sqls)
        conn.commit()
    cursor.close()
    conn.close()
map={"1" : "apple", "2" : "banana", "3" : "grape", "4" : "orange"}
list =()
for each in map:
    s = (each)
    list=s
print list
#updateFrequency(map)