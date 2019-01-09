from sklearn import svm 
import numpy as np 

num = 1
x_1 = np.load("npy/x_" + str(num) + ".npy")
y_1 = np.load("npy/y_" + str(num) + ".npy")

print(x_1)
print(x_1.shape)
print(y_1)
print(y_1.shape)
