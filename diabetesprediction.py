# -*- coding: utf-8 -*-
"""DiabetesPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ulATsqjqeqv0VQO0OhUTApEyKtnl2P3d

***Importing Dependencies***
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

"""***Data Collection and Analysis***"""

diabetes_dataset = pd.read_csv('/content/diabetes.csv')
diabetes_dataset.head()

diabetes_dataset.shape

diabetes_dataset.describe()

diabetes_dataset['Outcome'].value_counts()

diabetes_dataset.isnull().sum()

"""***Heat Map Generation and Finding out the Corelation between independent variables***"""

correlation = diabetes_dataset.corr()
plt.figure(figsize=(10,10))
sns.heatmap(correlation, cbar=True, square=True, fmt='.1f', annot=True, annot_kws={'size':8}, cmap='YlOrBr')

X=diabetes_dataset.drop(columns='Outcome',axis = 1)
Y=diabetes_dataset['Outcome']

print(X)
print(Y)

print(X.shape)
print(Y.shape)

"""***Data Standardization***"""

#scaler=StandardScaler()
#scaler.fit(X)
#standardized_data=scaler.transform(X)
#print(standardized_data)
#X=standardized_data
#Y=diabetes_dataset['Outcome']
#print(X)
#print(Y)

"""***Model Creation for different algorithms***

"""

LogisticRegressionModel=LogisticRegression(solver="liblinear" , max_iter=100)
#DecisionTreeClassifierModel=DecisionTreeClassifier()
#ClassifierModel=svm.SVC(kernel='linear')

"""***Splitting the Data***

***0.025 --> 1.0 Accuracy
   0.035 --> 0.96 Accuracy***
"""

X_train,x_test,Y_train,y_test=train_test_split(X,Y,test_size=0.035,random_state=0)
print(X.shape,X_train.shape,x_test.shape)
print(Y)

#K-Fold Cross Validation
#from sklearn.model_selection import KFold
#kfold_validation1=KFold(30)
#10 different splits with different random states
#from sklearn.model_selection import cross_val_score
#results1=cross_val_score(ClassifierModel,X,Y,cv=kfold_validation)
#results2=cross_val_score(LogisticRegressionModel,X,Y,cv=kfold_validation)
#results3=cross_val_score(DecisionTreeClassifierModel,X,Y,cv=kfold_validation)
#print('SVM = ',results1)
#print('Logistic Regression',results2)
#print('Decision Tree Classifier',results3)
#print(np.mean(results1))
#print(np.mean(results2))
#print(np.mean(results3))

"""**Using the above cell we find out that the Logistic Regression Model is more accurate when compared with SVM and Decision Tree Classifier. 
Later down the line we will further use Hyper Parameter Tuning to further increase the accuracy**

***Training the Model***
"""

LogisticRegressionModel.fit(X_train,Y_train)

"""***Evaluation the Model***"""

#Prediction on training data
predict1=LogisticRegressionModel.predict(X_train)
training_data_accuracy_score=accuracy_score(predict1,Y_train)
print(training_data_accuracy_score)

#Prediction on test data
predict2=LogisticRegressionModel.predict(x_test)
test_data_accuracy_score=accuracy_score(predict2,y_test)
print(test_data_accuracy_score)

"""***Making a Predictive System***"""

#OLD WITHOUT HYPER PARAMETERS
input_data=(6,148,72,35,0,33.6,0.627,50)
input_data_numpy=np.asarray(input_data)
input_data_reshaped=input_data_numpy.reshape(1,-1)
#print(input_data_reshaped)
predict=LogisticRegressionModel.predict(input_data_reshaped)
#print(predict)
if(predict[0]==0):
  print("Patient is Not Diabetic")
else:
  print("Patient is Diabetic")



"""***Hyperparameter Tuning***

Code Snippet below written by Author Enes Polat https://www.kaggle.com/enespolat
"""

grid=[{"C":np.logspace(-10,10,20), "penalty":["l1","l2"]}]# l1 lasso l2 ridge
logreg_cv=GridSearchCV(LogisticRegressionModel,grid,cv=10)
logreg_cv.fit(x_test,y_test)

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)

"""**Applying Parameters to the Model**

"""

update=LogisticRegression(solver = "liblinear", penalty = "l2", C=4.799818286283774)
update.fit(X_train,Y_train)
train_pred=update.predict(X_train)
test_pred=update.predict(x_test)
score=accuracy_score(test_pred,y_test)
print(score)

"""**Newer Prediction Model**"""

input_data=(1,103,30,38,83,43.3,0.183,33)
input_data_numpy=np.asarray(input_data)
input_data_reshaped=input_data_numpy.reshape(1,-1)
#print(input_data_reshaped)
predict1=update.predict(input_data_reshaped)
#print(predict)
if(predict1[0]==0):
  print("Patient is Not Diabetic")
else:
  print("Patient is Diabetic")