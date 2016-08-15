# coding=utf-8
# author = 'AaronChou'
import numpy as np

x = np.arange(4).reshape((2, 2))

x = np.transpose(x)

x = np.ones((1, 2, 3))
print x
image_size =  (3, 50, 50)
image_vector_len = np.prod(image_size)
x.transpose(2,0,1).reshape((image_vector_len, ))

#np.transpose(x, (1, 0, 2)).shape(2, 1, 3)
print x
