# -*- coding:utf-8 -*-
import sys
import os
import time
import numpy as np
from util import *
from datetime import datetime
from lstm_theano import LSTM_Theano

#
LEARNING_RATE = float(os.environ.get("LEARNING_RATE", "0.001"))
VOCABULARY_SIZE = int(os.environ.get("VOCABULARY_SIZE", "2000"))
EMBEDDING_DIM = int(os.environ.get("EMBEDDING_DIM", "48"))
HIDDEN_DIM = int(os.environ.get("HIDDEN_DIM", "128"))
NEPOCH = int(os.environ.get("NEPOCH", "20"))
MODEL_OUTPUT_FILE = os.environ.get("MODEL_OUTPUT_FILE")
INPUT_DATA_FILE = os.environ.get("INPUT_DATA_FILE",
                                 "../../../data/NLP/lstm_language_model/data/reddit-comments-2015-08.csv")
PRINT_EVERY = int(os.environ.get("PRINT_EVERY", "25000"))

if not MODEL_OUTPUT_FILE:
    ts = datetime.now().strftime("%Y-%m-%d-%H-%M")
    MODEL_OUTPUT_FILE = "LSTM-%s-%s-%s-%s.dat" % (ts, VOCABULARY_SIZE, EMBEDDING_DIM, HIDDEN_DIM)

# load data
x_train, y_train, word_to_index, index_to_word = load_data(INPUT_DATA_FILE, VOCABULARY_SIZE)

# build model
model = LSTM_Theano(VOCABULARY_SIZE, hidden_dim=HIDDEN_DIM, bptt_truncate=-1)

#
t1 = time.time()
model.sgd_step(x_train[10], y_train[10], LEARNING_RATE)
t2 = time.time()
print ("SGD 迭代时间为 %f 毫秒" % ((t2 - t1) * 1000))
sys.stdout.flush()


def sgd_callback(model, num_examples_seen):
    dt = datetime.now().isoformat()
    loss = model.calculate_loss(x_train[:10000], y_train[:10000])
    print("\n%s (%d)" % (dt, num_examples_seen))
    print("--------------------------------------------------")
    print("Loss: %f" % loss)
    generate_sentences(model, 10, index_to_word, word_to_index)
    save_model_parameters_theano(model, MODEL_OUTPUT_FILE)
    print("\n")
    sys.stdout.flush()


for epoch in range(NEPOCH):
    train_with_sgd(model, x_train, y_train, learning_rate=LEARNING_RATE, nepoch=1, decay=0.9,
                   callback_every=PRINT_EVERY, callback=sgd_callback)
