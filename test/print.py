#coding=gbk


sql="23s"

sqls="SELECT  d.personcode,d.jz_date,d.jbmc FROM disease  d WHERE d.personcode in("+sql+")and d.jz_date IN (SELECT jz_date from disease d WHERE d.personcode in ("+sql+")group by jz_date having count(*)>="+str(len(sql.split(",")))+");"

print sqls

a=1
b="2"
c="2"
if abs(a-int(b))<2 and b==c:
    print "yes"
