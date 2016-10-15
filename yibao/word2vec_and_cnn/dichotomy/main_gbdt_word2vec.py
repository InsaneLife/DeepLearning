# coding=utf8
import cPickle
from numpy import *
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing

import MySQLdb
import sys
from sklearn import ensemble
import word_match_vector
WEEKDAY = "isweekday"

reload(sys)
sys.setdefaultencoding('utf-8')


def excuteSql(sql):
    """

    :rtype : MySQL执行
    """
    sql = sql.encode("utf-8")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='tianchi', charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def getTrain():
    # sql = "select * from tianchi_r_10 r "
    sql = "select r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg,nextgs,rankul from tianchi_r_10 r GROUP BY r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg,nextgs,rankul"
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    train_x = []
    train_y = []
    for each in row:
        train_x.append([1.0, int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                        int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        train_y.append(int(each["nextgs"]))
    cursor.close()
    conn.close()
    # return mat(train_x), mat(train_y).transpose()
    return train_x, train_y


def get_test_1217():
    # sql = "select * from tianchi_r_10 r "
    sql = "select r.l,r.s,r.j,r.g,r.rankl,r.ranks,r.rankj,weekg,nextgs,rankul from test_1217 r"
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    train_x = []
    train_y = []
    for each in row:
        train_x.append([1.0, int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                        int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        train_y.append(int(each["nextgs"]))
    cursor.close()
    conn.close()
    # return mat(train_x), mat(train_y).transpose()
    return train_x, train_y


def getForcast():
    sql = "SELECT * FROM tianchi_fresh_test8 t "
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    row = cursor.fetchall()
    test_x = []
    x = []
    for each in row:
        test_x.append([1.0, int(each["l"]), int(each["s"]), int(each["j"]), int(each["g"]), int(each["rankl"]),
                       int(each["ranks"]), int(each["rankj"]), int(each["rankul"]), int(each["weekg"])])
        x.append([each["user_id"], each["item_id"]])
    cursor.close()
    conn.close()
    # return mat(test_x), x
    return test_x, x


def gbdt(X_train, y_train, deep, tree):
    # params = dict(original_params)
    # params.update({'learning_rate': 1.0, 'subsample': 1.0})
    # clf = ensemble.GradientBoostingClassifier(**params)
    # clf.fit(X_train, y_train)

    clf = ensemble.GradientBoostingClassifier(n_estimators=tree, learning_rate=0.01, loss='exponential',
                                              max_depth=deep, random_state=0).fit(X_train, y_train)
    return clf


def insertMysql(t):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='admin', db='tianchi')
    cursor = conn.cursor()
    sql1 = "insert into tianchi_predict4 values(%s,%s,%s)"
    for each in t:
        # sql = "insert into tianchi_mobile_recommendation_predict2 values('"+str(each[0])+"','"+str(each[1])+"','"+str(each[2])+"')"
        cursor.execute(sql1, each)
    conn.commit()
    cursor.close()
    conn.close()


def simple_sampling(dataMat, num):
    try:
        samples = random.sample(dataMat, num)
        return samples
    except:
        print('sample larger than population')


def gbdt_tarin_save(deep, tree):
    ## step 2: training...
    print "Training..."
    # opts = {'alpha': 0.01, 'maxIter': 20, 'optimizeType': 'smoothStocGradDescent'}
    # optimalWeights = trainLogRegres(train_x, train_y, opts)
    train_x, train_y = getTrain()
    i = 4
    while (i < 6):
        j = 150
        while (j < 300):
            gbdtmodel = gbdt(train_x, train_y, i, j)
            model_name = "gbdt"
            with open("model//" + model_name + '_' + str(i) + '_' + str(j), 'wb') as f_handle:
                print 'Saving model...'
                sys.setrecursionlimit(2000)
                cPickle.dump(gbdtmodel, f_handle, protocol=cPickle.HIGHEST_PROTOCOL)
            j += 25
        i += 1


def gbdt_test1217(threshold, gbdtmodel):
    print "Testing..."
    test1217_x, label = get_test_1217()
    predicty_1217 = gbdtmodel.predict_proba(test1217_x)[:, 1]  # probablity of 1
    predict_num = 0
    right_num = 0
    reference_num = 0
    test_len = predicty_1217.__len__()
    for i in xrange(test_len):
        if predicty_1217[i] > threshold:
            predict_num += 1
            if label[i] == 1:
                right_num += 1
        if label[i] == 1:
            reference_num += 1
    precision = float(right_num) / predict_num
    reference = float(right_num) / reference_num
    f1 = 2 * precision * reference / (precision + reference)
    print f1, predict_num


startTime = time.time()
forcasts = []
# get data


## step 2: training...
model_name = "gbdt"
deep = 4
tree = 150
X_train, y_train, x_test, y_test = word_match_vector.get_gbdt_data()
gbdtmodel = gbdt(X_train, y_train, deep, tree)

threshold = 0.207458979001
while threshold < 0.42:
    #gbdt_test1217(threshold, gbdtmodel)
    threshold += 0.01
#print s
# step 4: make Forecast
print "Forecasting..."
test_x, x = getForcast()
# forcast = makeyuce(optimalWeights, test_x  ,x)
# forcasts.append(forcast)
# if(forcast.__len__()):
#     break
predicty = gbdtmodel.predict_proba(test_x)[:, 1]  # probablity of 1
for i in xrange(predicty.__len__()):
    forcasts.append([x[i][0], x[i][1], predicty[i]])
print forcasts.__len__()

## write the result
# output=open('C:\\Users\\bean\\Desktop\\tianchi_mobile_recommendation_predict.csv','w')
# #putDate = json.dumps(putDate,ensure_ascii=False,indent=4)
# output.write('user_id,item_id\n')
# for forcast in forcasts:
#     #output.write(str(each[0])+','+str(each[1])+'\n')
#     for each in forcast:
#         text = str(each[0])+","+str(each[1])+","+str(each[2])+"\n"
#         output.write(text)
# output.close()
print "Insert Mysql..."
excuteSql("TRUNCATE TABLE tianchi_predict4")
insertMysql(forcasts)
print 'Took %fs!' % (time.time() - startTime)
