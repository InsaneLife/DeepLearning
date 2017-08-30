# coding=utf8
"""
author=Aaron
python=3.5
TensorFlow=1.2.1
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


# 产生随机变量，符合 normal 分布
# 传递 shape 就可以返回weight和bias的变量
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# 定义2维的 convolutional 图层
def conv2d(x, W):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[3] = 1
    # strides 就是跨多大步抽取信息
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


# 定义 pooling
def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    # 用pooling对付跨步大丢失信息问题
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# 读取数据
mnist = input_data.read_data_sets("D:/data/minist/", one_hot=True)

# 为输入图像和目标输出类别创建节点，来开始构建计算图。x和y是占位符
x = tf.placeholder("float", shape=[None, 784])  # 784＝28x28
y_ = tf.placeholder("float", shape=[None, 10])

'''1. conv1 layer'''
#  把x_image的厚度1加厚变成了32
W_conv1 = weight_variable([5, 5, 1, 32])  # patch 5x5, in size 1, out size 32
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1, 28, 28, 1])  # 最后一个1表示数据是黑白的
# 构建第一个convolutional层，然后加一个非线性化的处理relu
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # output size 28x28x32
# 经过pooling后，长宽缩小为14x14
h_pool1 = max_pool_2x2(h_conv1)  # output size 14x14x32

'''2. conv2 layer'''
# 把厚度32加厚变成了64
W_conv2 = weight_variable([5, 5, 32, 64])  # patch 5x5, in size 32, out size 64
b_conv2 = bias_variable([64])
# 构建第二个convolutional层
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)  # output size 14x14x64
# 经过pooling后，长宽缩小为7x7
h_pool2 = max_pool_2x2(h_conv2)  # output size 7x7x64

'''3. func1 layer'''
# 变成1024
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
# [n_samples, 7, 7, 64] ->> [n_samples, 7*7*64]
# 把pooling后的结果变平
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

'''4. func2 layer'''
# 最后一层，输入1024，输出size 10，用 softmax 计算概率进行分类的处理
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
# 向量化后的图片x和权重矩阵W相乘，加上偏置b，然后计算每个分类的softmax概率值。
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# 损失函数定义为交叉熵
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
# 最梯度下降法让交叉熵下降，步长为0.01
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)  # 3333333333 test accuracy 0.9922
# train_step = tf.train.GradientDescentOptimizer(1e-3).minimize(cross_entropy)
# 计算分类的准确率，tf.equal 来检测我们的预测是否真实标签匹配
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
# 计算出匹配结果correct_prediction的平均值为，如[1,0,1,1]为0.75
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# 创建一个Saver对象，选择性保存变量或者模型。
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    # 输出最终模型在测试集上的准确率
    print("test accuracy %g" % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

    # 保存模型到model.ckpt
    save_path = saver.save(sess, "model/model.ckpt")
    print("Model saved in file: ", save_path)

# with tf.Session() as sess:
#     # 读取模型
#     saver.restore(sess, "model/model.ckpt")
#     print("Model restored.")
#
#     # 输出最终模型在测试集上的准确率
#     print("test accuracy %g" % accuracy.eval(feed_dict={
#         x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
