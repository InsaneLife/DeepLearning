# coding=utf8
# author = 'AaronChou'
from numpy import *
import matplotlib.pyplot as plt
import time
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def max_sum(arr):
    if arr.__len__()==0 or arr == None:
        return 0
    max = 0
    cur = 0
    for each in arr:
        cur += each
        if cur > max:
            max = cur
        if cur <0:
            cur = 0
    return max

arr = [-1,2,1,-1,3,1]
sum = max_sum(arr)
print sum