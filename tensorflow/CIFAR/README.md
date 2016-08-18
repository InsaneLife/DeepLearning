CIFAR-10 is a common benchmark in machine learning for image recognition.

http://www.cs.toronto.edu/~kriz/cifar.html

Code in this directory demonstrates how to use TensorFlow to train and evaluate a convolutional neural network (CNN) on both CPU and GPU. We also demonstrate how to train a CNN over multiple GPUs.

Detailed instructions on how to get started available at:

http://tensorflow.org/tutorials/deep_cnn/

cifar10_input.py 	读取本地CIFAR-10的二进制文件格式的内容。
cifar10.py 	建立CIFAR-10的模型。
cifar10_train.py 	在CPU或GPU上训练CIFAR-10的模型。
cifar10_multi_gpu_train.py 	在多GPU上训练CIFAR-10的模型。
cifar10_eval.py 	评估CIFAR-10模型的预测性能。