from sklearn import preprocessing 
from sklearn import svm,metrics
from sklearn.model_selection import train_test_split
import numpy as np 
from sklearn.externals import joblib

num = 1
x = np.load("npy_20190605/x_" + str(num) + ".npy")
y = np.load("npy_20190605/y_" + str(num) + ".npy")

for i in range(1,17):
	x_now = np.load("npy_20190605/x_" + str(i+1) + ".npy")
	y_now = np.load("npy_20190605/y_" + str(i+1) + ".npy")
	x = np.vstack((x,x_now)) 
	y = np.vstack((y,y_now))

#print(x)
#print(x.shape)
#print(y)
#print(y.shape)

#print(x[0:1])
#print(preprocessing.scale(x[0:1]))


#x = preprocessing.scale(x)
#print(x)
#x = (x - x.min(1).reshape(-1,1))/(x.max(1).reshape(-1,1)-x.min(1).reshape(-1,1))
#print(x)
x_train , x_test, y_train, y_test = train_test_split(x , y , test_size = 0.1)

svc = svm.SVC(kernel='linear',degree=3 ,C=0.1, gamma=0.1)
svc_fit = svc.fit(x_train, y_train)

y_predicted = svc.predict(x_test)

for i in range(y_test.shape[0]):
	print("real:%d predicted:%d" %(y_test[i],y_predicted[i]))
accuracy = metrics.accuracy_score(y_test,y_predicted)
print("accuracy: %f "%(accuracy))
joblib.dump(svc_fit, 'model/svc_20190605.pkl') 
