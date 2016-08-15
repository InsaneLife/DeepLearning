__author__ = 'Bean'
# coding: utf-8

import sys
import os
from get_feature import *

from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn import cross_validation, ensemble

import cPickle


def gbdt(x, y):
    clf = ensemble.GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=0).fit(x,
                                                                                                                    y)
    return clf


def gbdt_train_save(test_set_file, estimator_file='svm_classifier'):
    train_folder = 'E:/soft/Project/zte/ztedata/youtube/result_folder/'
    model_name = 'model/gbdt_youtube_d5_t200'
    train_vector, train_label = get_train_data(train_folder)
    # print train_label.__len__()

    gbdt_model = gbdt(train_vector, train_label)
    with open(model_name, 'wb') as f_handle:
        print 'Saving model...'
        sys.setrecursionlimit(2000)
        cPickle.dump(gbdt_model, f_handle, protocol=cPickle.HIGHEST_PROTOCOL)
        print 'Saving model complete'


def get_model_and_predict(estimator_file):
    with open(estimator_file, 'rb') as f:
        gbdt_model = cPickle.load(f)
    test_folder = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_result_folder/'
    zte_datalist_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/datalist.txt'
    zte_rgb_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file.csv'

    test_vector, test_label = get_zte_test(zte_datalist_path, zte_rgb_path, test_folder)

    predicty = gbdt_model.predict_proba(test_vector)[:, 1]
    f = open('E:/soft/Project/zte/ztedata/zte_face_test/test1/zte_output.txt', 'w')
    for i in xrange(predicty.__len__()):
        text = str(i) + "," + str(predicty[i]) + "," + str(test_label[i]) + "\n"
        f.write(str(text))
    f.close()
    print gbdt_model.score(test_vector, test_label)


if __name__ == "__main__":
    # gbdt_train_save(('/ZTE_croped_images/people_1_vector_160', ''))
    get_model_and_predict('model/gbdt_youtube_d5_t200')