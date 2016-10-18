# coding=utf8
# author = 'Aaron Chou'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_word_vector(path="..//../../data/yibao/word2vec/kc25k2_oneline_cut_out.txt"):
    word_vector_map = {}
    with open(path) as f:
        for line in f:
            # UNK	0.138251,-0.0511282,0.134034,-0.00142783...
            word = line.strip("\n").split("\t")[0]
            vector = line.strip("\n").split("\t")[1].split(",")
            word_vector_map[word] = vector
    return word_vector_map


def get_sentence_vector():
    word_vector_map = get_word_vector()

    word_vectors = []
    label = []
    disease_map = {}
    class_index = 0
    file_path = '../..//../data/yibao/word2vec/ykc100_cut_top10.txt'
    out_path = '../../..//data/yibao/word2vec/word2vec_and_cnn/ykc100_cut_vector_top10.txt'
    out = open(out_path,'w')
    with open(file_path) as f:
        for line in f:
            # J20.900,咳嗽 10 天
            disease = line.split(",")[0]
            if disease_map.has_key(disease) == 0:
                disease_map[disease] = class_index
                class_index += 1

            words = line.strip("\n").strip(" ").split(",")[1].split(" ")
            if words.__len__() > 32:
                words = words[:32]
            vectors = [0 for i in range(4096)]
            i = 0
            for word in words:
                for v in word_vector_map[word]:
                    vectors[i] = float(v)
                    i += 1
            out.write(str(disease_map[disease])+","+str(vectors)+"\n")
            # word_vectors.append(vectors)
            # label.append(disease_map[disease])

    out.close()
get_sentence_vector()