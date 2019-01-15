from sklearn.externals import joblib
import numpy as np
svc_fit = joblib.load('model/svc_0115.pkl') 
x=np.array([[-0.3,-0.4,-0.1,-0.7,-0.25,-0.1]])
print(svc_fit.predict(x))
