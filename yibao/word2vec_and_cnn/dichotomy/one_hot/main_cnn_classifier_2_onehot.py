# coding=utf8
# author = 'Aaron Chou'
import os
import sys

import time

reload(sys)
sys.setdefaultencoding('utf-8')

import tensorflow as tf
import input_data


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 4, 4, 1], strides=[1, 4, 4, 1], padding='SAME')


sess = tf.InteractiveSession()
x = tf.placeholder("float", shape=[None, 25600])
y_ = tf.placeholder("float", shape=[None, 2])

x_image = tf.reshape(x, [-1, 160, 160, 1])
W_conv1 = weight_variable([7, 7, 1, 16])
b_conv1 = bias_variable([16])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([6, 6, 16, 32])
b_conv2 = bias_variable([32])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([10 * 10 * 32, 256])
b_fc1 = bias_variable([256])
h_pool2_flat = tf.reshape(h_pool2, [-1, 10 * 10 * 32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
W_fc2 = weight_variable([256, 2])
b_fc2 = bias_variable([2])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)  # test accuracy 0.9922
# train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
predict = tf.argmax(y_conv, 1)

# Add an op to initialize the variables.
init_op = tf.initialize_all_variables()

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

# load data
mnist = input_data.read_data_sets(one_hot=True)

# Later, launch the model, initialize the variables, do some work, save the
# variables to disk.
parm = "VALID_c8*8_p2*2_f16_o256"
model_path = "../../../../data/yibao/word2vec/word2vec_and_cnn/model_2_onehot/" + parm + "/"
if not os.path.exists(model_path):
    os.makedirs(model_path)
with tf.Session() as sess:
    sess.run(init_op)
    # saver.restore(sess, "../../../mnist//model/model31000.ckpt")
    time1 = time.time()
    for i in range(50000):
        batch = mnist.train.next_batch(50)
        model_name = model_path + str(i) + ".ckpt"
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print "step %d, training accuracy %g" % (i, train_accuracy)
            time2 = time.time()
            # print time2 - time1
            time1 = time2
            # if accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}) > 0.999:
            #     break
        if i % 1000 == 0:
            save_path = saver.save(sess, model_name)
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print "test accuracy %g" % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})

    # Save the variables to disk.
    save_path = saver.save(sess, model_name)
    print "Model saved in file: ", save_path

model_name = "../../../../data/yibao/word2vec/word2vec_and_cnn/model_2_onehot/3000.ckpt"
with tf.Session() as sess:
    # Restore variables from disk.
    saver.restore(sess, model_name)
    print "Model restored."
    print "test accuracy %g" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})
