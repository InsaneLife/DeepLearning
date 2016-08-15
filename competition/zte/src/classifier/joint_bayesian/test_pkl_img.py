# coding=utf-8
import sys
import numpy as np
from common import *
from scipy.io import loadmat
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from joint_bayesian import *
from get_feature import *
import cPickle


def excute_train(train_data, result_fold="result_img/"):
    data, label = get_pca_data(train_data)
    data = np.array(data)
    label = np.array(label)
    print data.shape, label.shape

    # data predeal
    data = data_pre(data)

    # pca training
    pca = PCA_Train(data, result_fold)
    data_pca = pca.transform(data)

    data_to_pkl(data_pca, result_fold + "pca_wdref.pkl")
    JointBayesian_Train(data_pca, label, result_fold)


def excute_zte_test(test_folder, zte_datalist_path, zte_rgb_path, result_fold="result_img/"):
    # print os.listdir(result_fold), result_fold + "A.pkl"
    with open(result_fold + "A.pkl", "r") as f:
        A = pickle.load(f)
    with open(result_fold + "G.pkl", "r") as f:
        G = pickle.load(f)


    test_Intra, test_Extra ,data = get_zte_rgb_test(zte_datalist_path, zte_rgb_path, test_folder)

    test_Intra = np.array(test_Intra)
    test_Extra = np.array(test_Extra)
    data = np.array(data)

    print test_Intra.shape, test_Extra.shape, data.shape

    data = data_pre(data)

    clt_pca = joblib.load(result_fold + "pca_model.m")
    data = clt_pca.transform(data)
    # data_to_pkl(data, result_fold + "pca_lfw.pkl")
    # data = read_pkl(result_fold + "pca_lfw.pkl")
    print data.shape

    dist_Intra = get_ratios(A, G, test_Intra, data)
    dist_Extra = get_ratios(A, G, test_Extra, data)

    dist_all = dist_Intra + dist_Extra
    dist_all = np.asarray(dist_all)
    label = np.append(np.repeat(1, len(dist_Intra)), np.repeat(0, len(dist_Extra)))

    data_to_pkl({"distance": dist_all, "label": label}, result_fold + "zte_result.pkl")


def excute_test(pairlist="E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file_vector/0.pkl",
                test_data="E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file_vector/1.pkl",
                result_fold="result/"):
    print os.listdir(result_fold), result_fold + "A.pkl"
    # f = open(result_fold+"A_con.pkl", "rb")
    # A = cPickle.load(f)
    # f = open(result_fold+"G_con.pkl", "rb")
    # G = cPickle.load(f)
    with open(result_fold + "A.pkl", "r") as f:
        A = pickle.load(f)
    with open(result_fold + "G.pkl", "r") as f:
        G = pickle.load(f)

    with open(test_data, "rb") as f:
        data, label = cPickle.load(f)

    test_Intra = np.array([0])
    test_Extra = np.array([0])

    print test_Intra, test_Intra.shape
    print test_Extra, test_Extra.shape

    data = data_pre(data)

    clt_pca = joblib.load(result_fold + "pca_model.m")
    data = clt_pca.transform(data)
    data_to_pkl(data, result_fold + "pca_lfw.pkl")

    data = read_pkl(result_fold + "pca_lfw.pkl")
    print data.shape

    dist_Intra = get_ratios(A, G, test_Intra, data)
    dist_Extra = get_ratios(A, G, test_Extra, data)

    dist_all = dist_Intra + dist_Extra
    dist_all = np.asarray(dist_all)
    label = np.append(np.repeat(1, len(dist_Intra)), np.repeat(0, len(dist_Extra)))

    data_to_pkl({"distance": dist_all, "label": label}, result_fold + "result.pkl")


if __name__ == "__main__":
    train_data='E:/soft/Project/zte/ztedata/img/train_set_file_vector/'
    test_folder = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file_vector/'
    zte_datalist_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/datalist.txt'
    zte_rgb_path = 'E:/soft/Project/zte/ztedata/zte_face_test/test1/rgb_set_file.csv'
    excute_train(train_data)
    excute_zte_test(test_folder, zte_datalist_path, zte_rgb_path)
    excute_performance("result_img/zte_result.pkl", -16.9, -16.6, 0.01)
