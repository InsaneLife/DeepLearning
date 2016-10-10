#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('gbk')

path="C://Users//bean//Desktop//output.json"
f2=open(path,'r')
zz = json.load(f2)
f2.close()

for each in zz[0]:
    s=""
    for every in each["personCodes"]:
        s+=every+","
    print s[:-1]
    print each["supportdeg"]



path="E:\\Datamining\\ssss.txt"
#json.dump(list, open(path, 'w'))

# s=json.dumps(list)
# f=open(path,'w')
# f.write(s)
