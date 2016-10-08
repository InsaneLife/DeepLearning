# -*- coding:utf-8 -*-
import csv
import itertools
import numpy as np
import nltk
import time
import sys
import operator
import io
import array
from datetime import datetime
from  lstm_theano import LSTM_Theano


SENTENCE_START_TOKEN = "SENTENCE_START"
SENTENCE_END_TOKEN = "SENTENCE_END"
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

def load_data(filename="../../../data/NLP/lstm_language_model/data/reddit-comments-2015-08.csv", vocabulary_size=2000, min_sent_characters=0):

    word_to_index = []
    index_to_word = []

    #读取文件内容
    print("Reading CSV file...")
    with open(filename ,'rt') as f:
        reader = csv.reader(f, skipinitialspace=True)
        reader.next()
        sentences=itertools.chain(*[nltk.sent_tokenize(x[0].decode("utf-8").lower()) for x in reader])
        #过滤掉一些句子，如长度不符合等
        sentences=[s  for s in sentences if len(x)>min_sent_characters]
        sentences=[s for s in sentences if "http" not in s]
        #给每个句子加上开头和结束符号
        sentences =["%s %s %s"% (SENTENCE_START_TOKEN,s,SENTENCE_END_TOKEN) for s in sentences]
    print ("一共有%d个句子" %(len(sentences)))

    #对句子进行分词
    tokenized_sentences=[ nltk.word_tokenize(s) for s in sentences]

    #统计词频
    word_freq=nltk.FreqDist(nltk.chain(*tokenized_sentences)) #注意nltk.FreqDist只能读取一级列表
    print("词频")
    #选取词频高的.选取前面的vocabulary_size个高频词作为词表
    vocab=sorted(word_freq.items(),key= lambda x:(x[1],x[0]),reverse=True)[:vocabulary_size-2] #这里减去2是为了后面还要加上</MASK>和UNKNOW_TOKEN
    print("词表的长度为：%d" %(vocabulary_size))
    sorted_vocab=sorted(vocab,key=operator.itemgetter(1))

    #词表
    index_to_word = ["<MASK/>", UNKNOWN_TOKEN] + [x[0] for x in sorted_vocab]
    #词表的位置
    word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])
    for i ,sent in enumerate(tokenized_sentences):
        tokenized_sentences[i]=[w if w in index_to_word else UNKNOWN_TOKEN for w in sent]

    # 生成训练数据和标签
    X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
    y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])

    return X_train, y_train, word_to_index, index_to_word

def train_with_sgd(model,X_train,y_train,learning_rate=0.001, nepoch=20, decay=0.9,
    callback_every=10000, callback=None):
    num_example_seen=0
    for epoch in range(nepoch):
        #随机梯度下降
        for i in np.random.permutation(len(y_train)):
            model.sgd_step(X_train[i],y_train[i],learning_rate,decay)
            num_example_seen+=1
            #回调函数
            if(callback and callback_every and num_example_seen%callback_every==0):
                callback(model,num_example_seen)
    return model

#保存model
def save_model_parameters_theano(model, outfile):
    np.savez(outfile,
        E=model.E.get_value(),
        U=model.U.get_value(),
        W=model.W.get_value(),
        V=model.V.get_value(),
        b=model.b.get_value(),
        c=model.c.get_value())
    print "保存模型参数至于  %s." % outfile

#加载模型参数

def load_model_ameters_theano(path, modelClass=LSTM_Theano):
    npzfile = np.load(path)
    E, U, W, V, b, c = npzfile["E"], npzfile["U"], npzfile["W"], npzfile["V"], npzfile["b"], npzfile["c"]
    hidden_dim, word_dim = E.shape[0], E.shape[1]
    print "Building model model from %s with hidden_dim=%d word_dim=%d" % (path, hidden_dim, word_dim)
    sys.stdout.flush()
    model = modelClass(word_dim, hidden_dim=hidden_dim)
    model.E.set_value(E)
    model.U.set_value(U)
    model.W.set_value(W)
    model.V.set_value(V)
    model.b.set_value(b)
    model.c.set_value(c)
    return model

#检查梯度
def gradient_check_theano(model, x, y, h=0.001, error_threshold=0.01):
    # Overwrite the bptt attribute. We need to backpropagate all the way to get the correct gradient
    model.bptt_truncate = 1000
    # Calculate the gradients using backprop
    bptt_gradients = model.bptt(x, y)
    # List of all parameters we want to chec.
    model_parameters = ['E', 'U', 'W', 'b', 'V', 'c']
    # Gradient check for each parameter
    for pidx, pname in enumerate(model_parameters):
        # Get the actual parameter value from the mode, e.g. model.W
        parameter_T = operator.attrgetter(pname)(model)
        parameter = parameter_T.get_value()
        print "Performing gradient check for parameter %s with size %d." % (pname, np.prod(parameter.shape))
        # Iterate over each element of the parameter matrix, e.g. (0,0), (0,1), ...
        it = np.nditer(parameter, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            ix = it.multi_index
            # Save the original value so we can reset it later
            original_value = parameter[ix]
            # Estimate the gradient using (f(x+h) - f(x-h))/(2*h)
            parameter[ix] = original_value + h
            parameter_T.set_value(parameter)
            gradplus = model.calculate_total_loss([x],[y])
            parameter[ix] = original_value - h
            parameter_T.set_value(parameter)
            gradminus = model.calculate_total_loss([x],[y])
            estimated_gradient = (gradplus - gradminus)/(2*h)
            parameter[ix] = original_value
            parameter_T.set_value(parameter)
            # The gradient for this parameter calculated using backpropagation
            backprop_gradient = bptt_gradients[pidx][ix]
            # calculate The relative error: (|x - y|/(|x| + |y|))
            relative_error = np.abs(backprop_gradient - estimated_gradient)/(np.abs(backprop_gradient) + np.abs(estimated_gradient))
            # If the error is to large fail the gradient check
            if relative_error > error_threshold:
                print "Gradient Check ERROR: parameter=%s ix=%s" % (pname, ix)
                print "+h Loss: %f" % gradplus
                print "-h Loss: %f" % gradminus
                print "Estimated_gradient: %f" % estimated_gradient
                print "Backpropagation gradient: %f" % backprop_gradient
                print "Relative Error: %f" % relative_error
                return
            it.iternext()
        print "Gradient check for parameter %s passed." % (pname)

def generate_sentence(model,index_to_word,word_to_index,min_length=5):
    new_sentence=[word_to_index[SENTENCE_START_TOKEN]]

    #重复循环生成句子
    while not new_sentence[-1] == word_to_index[SENTENCE_END_TOKEN]:
        next_word_probs=model.predict(new_sentence)[-1]
        samples=np.random.multinomial(1,next_word_probs) #generate multinomial distribution
        sample_word=np.argmax(samples)
        #put the new word into new_sentence
        new_sentence.append(sample_word)

        if len(new_sentence)>100:
            return None
    if len(new_sentence)<min_length:
        return None
    return new_sentence
#print the senetence
def print_sentence(s,index_to_word):
    sentence_str=[index_to_word[i] for i in s]
    print(" ".join(sentence_str))
    sys.stdout.flush()

#generate sentences
def generate_sentences(model,n,index_to_word,word_to_index):
    for i in range(n):
        sent=None
        while not sent:
            sent=generate_sentence(model,index_to_word,word_to_index)
        print_sentence(sent,index_to_word)




