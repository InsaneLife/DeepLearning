# coding=utf8
# author = 'Aaron Chou'
import sys
from sklearn.decomposition import PCA
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')

path= '../../../../data/NLP/sougou/result/news_oneline_cut_out.txt'
out_path= '../../../../data/NLP/sougou/result/news_oneline_cut_scatter_out.txt'

words = []
vectors = []
threshold = 1000
i = 0
with open(path) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split('\t')
        words.append(line[0])
        vectors.append(line[1].split(','))
        i += 1
        if i == threshold:
            break

words = np.array(words)
vectors = np.array(vectors)

pca = PCA(n_components=2)
vectors = pca.fit_transform(vectors)

with open(out_path, 'w') as out:
    for i in range(len(vectors)):
        out.write("[" + str(vectors[0]) + "," + str(vectors[1]) + ", 20000000, '" + words[0] + "'],")