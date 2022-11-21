# -*- coding: utf-8 -*-
"""Homework06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vO_tw2sCj2B9RMrru-1O3qVTFseevZcF
"""

import pandas as pd
import numpy as np
df = pd.read_csv('Dataset.csv',sep=",")

# Data Inspection
df.head()

df.columns

df.info()

df.describe()

# Check the correlation between variables
df1=df.corr(method='pearson', min_periods=1)
df1

# Matrix visualization
import matplotlib.pyplot as plt
plt.matshow(df1)

"""For Highly correlated features in the data, I have considered points more that 0.8 for positive correlation and points more that 0.4 for negative correlations. There are a total of 6 - 10 highly correlated features in the data."""

# Boxplot
df.boxplot()

"""Feature scaling is required in this data. 
For feature 7,6,4 should be taken into consideration. 

Real-world datasets often contain features that are varying in degrees of magnitude, range and units. Therefore, in order for machine learning models to interpret these features on the same scale, we need to perform feature scaling


"""

# Visualize the histogram
df.hist(bins=50, figsize=(20,15))

# Dividing the dataset into separate training and test dataset
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df[["Feature_1","Feature_2","Feature_3","Feature_4","Feature_5","Feature_6","Feature_7","Feature_8","Feature_9","Feature_10","Feature_11"]], df['Target_out'], test_size=0.3, random_state=10)

x_train

x_test

# we need to prepare the input features (X) and output labels (Y) for supervised learning
train_labels = df["Target_out"] # get labels for output label Y
train_features = df.drop(columns="Target_out") # drop labels to get features X for training set

# MinMax
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler() ## define the transformer
scaler.fit(x_train) ## call .fit() method to calculate the min and max value for each column in dataset
x_train_normalized = scaler.transform(x_train)
x_train_normalized=pd.DataFrame(x_train_normalized)
x_train_normalized.boxplot()

x_test_normalized = scaler.transform(x_test)
x_test_normalized=pd.DataFrame(x_test_normalized)
x_test_normalized.boxplot()

# Binary classification dataset by cutting the target values into two categories (<6, >=6)
y_train[y_train<6] = 0
y_train[y_train>=6] = 1

y_test[y_test<6] = 0
y_test[y_test>=6] = 1

y_train

# Logistic regression
from sklearn.linear_model import LogisticRegression
logistic_model = LogisticRegression(penalty = 'l2', C = 1, random_state = 0)
logistic_model.fit(x_train_normalized,y_train)
logistic_model.predict(x_test_normalized)

logistic_model.score(x_train_normalized,y_train)

"""A Logistic Regression is a sigmoid function which can divide 2 classes like linear regression. It takes a condition and if the condition is passed it goes into true class if not false class.

Theta = -(1/n) summation from 1 to n [y(i)log(p(i))+(1-y(i))log(1-p(i))]
"""

# Support Vector Machine
from sklearn.svm import SVC
# define linear kernel, P156
svm_model_linear = SVC(C = 1 ) 
svm_model_linear.fit(x_train_normalized,y_train)
svm_model_linear.predict(x_test_normalized)
svm_model_linear.score(x_train_normalized,y_train)

# define polynomial kernel, P158
svm_model_polynomial = SVC(kernel = "poly", degree = 3, C = 5 ) 
svm_model_polynomial.fit(x_train_normalized,y_train)
svm_model_polynomial.predict(x_test_normalized)
svm_model_polynomial.score(x_train_normalized,y_train)

svm_model_rbf = SVC(kernel = "rbf", gamma = 5, C = 2 ) 
svm_model_rbf.fit(x_train_normalized,y_train)
svm_model_rbf.predict(x_test_normalized)
svm_model_rbf.score(x_train_normalized,y_train)

"""The objective of SVM to find the optimal linear classifier is to find a hyperplane which is a line for a linear classifier which differentiates the two classifiers.

Linear, Non-Linear, polynomial kernel, Gaussian RBF kernel are available kernel functions for SVM to conduct linear and non-linear classification
"""

#Decision Tree
from sklearn.tree import DecisionTreeClassifier
decision_tree_model = DecisionTreeClassifier(max_depth = 3) # define tree model
decision_tree_model.fit(x_train_normalized,y_train)
decision_tree_model.predict(x_test_normalized)
decision_tree_model.score(x_train_normalized,y_train)

"""Step1: Determine the Root of the Tree, Step2: Calculate Entropy for The Classes, Step3: Calculate Entropy After Split for Each Attribute
Step4: Calculate Information Gain for each split , Step5: Perform the Split
Step6: Perform Further Splits, Step7: Complete the Decision Tree. Features are selected through feature space by ranking their mutual information with the ranked once.

The decision tree's hyper-parameters, such as max depth, min samples leaf, and min samples split, can be adjusted to stop the tree's growth early and stop the model from overfitting. Pre-pruning, which results in a tree with fewer branches than would otherwise be the case, and post-pruning are the two techniques for overcoming overfitting (generating a tree in full and then removing parts of it).
"""

# Random Forest
from sklearn.ensemble import RandomForestClassifier
random_forest_model = RandomForestClassifier(n_estimators = 100, max_leaf_nodes = 18)
random_forest_model.fit(x_train_normalized,y_train)
random_forest_model.predict(x_test_normalized)
random_forest_model.score(x_train_normalized,y_train)

"""Ensemble learning methods work by combining the mapping functions learned by contributing members.
Ensembles for classification are best understood by the combination of decision boundaries of members.
Ensembles for regression are best understood by the combination of hyperplanes of members.

It divides up the training set into smaller groups that solely contain particular features. The training set is sampled at random from with replacement to select the desired number of features. The random patches method is what is used when the random subspace method is combined with bagging or pasting.

It is determined as the node impurity reduction multiplied by the likelihood of reaching that node. The node probability can be computed by dividing the total number of samples by the number of samples that reach the node. The feature is more significant the higher the value.

"""

# K Nearest-neighbors
from sklearn.neighbors import KNeighborsClassifier
knn_model = KNeighborsClassifier(n_neighbors = 5, metric = "minkowski")
knn_model.fit(x_train_normalized,y_train)
knn_model.predict(x_test_normalized)
knn_model.score(x_train_normalized,y_train)

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
# Logistic regression - performance on the test data
logistic_pred = logistic_model.predict(x_test_normalized)
logistic_acc = accuracy_score(y_test, logistic_pred )
logistic_prec = precision_score(y_test, logistic_pred )
logistic_recall = recall_score(y_test, logistic_pred )
logistic_roc = roc_auc_score(y_test, logistic_pred )
logistic_f1 = f1_score(y_test, logistic_pred )
print(logistic_acc)
print(logistic_prec)
print(logistic_recall)
print(logistic_roc)
print(logistic_f1)

# SVM - performance on the test data

svm_pred = svm_model_linear.predict(x_test_normalized)
svm_acc = accuracy_score(y_test, svm_pred )
svm_prec = precision_score(y_test, svm_pred )
svm_recall = recall_score(y_test, svm_pred )
svm_roc = roc_auc_score(y_test, svm_pred )
svm_f1 = f1_score(y_test, svm_pred )
print(svm_acc)
print(svm_prec)
print(svm_recall)
print(svm_roc)
print(svm_f1)

# KNN - performance on the test data

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
knn_model_pred = knn_model.predict(x_test_normalized)
knn_model_acc = accuracy_score(y_test, knn_model_pred )
knn_model_prec = precision_score(y_test, knn_model_pred )
knn_model_recall = recall_score(y_test, knn_model_pred )
knn_model_roc = roc_auc_score(y_test, knn_model_pred )
knn_model_f1 = f1_score(y_test, knn_model_pred )
print(knn_model_acc)
print(knn_model_prec)
print(knn_model_recall)
print(knn_model_roc)
print(knn_model_f1)

# Decision Tree - performance on the test data

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
decision_tree_model_pred = decision_tree_model.predict(x_test_normalized)
decision_tree_model_acc = accuracy_score(y_test, decision_tree_model_pred )
decision_tree_model_prec = precision_score(y_test, decision_tree_model_pred )
decision_tree_model_recall = recall_score(y_test, decision_tree_model_pred )
decision_tree_model_roc = roc_auc_score(y_test, decision_tree_model_pred )
decision_tree_model_f1 = f1_score(y_test, decision_tree_model_pred )
print(decision_tree_model_acc)
print(decision_tree_model_prec)
print(decision_tree_model_recall)
print(decision_tree_model_roc)
print(decision_tree_model_f1)

# Random Forest - performance on the test data

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
random_forest_model_pred = random_forest_model.predict(x_test_normalized)
random_forest_model_acc = accuracy_score(y_test, random_forest_model_pred )
random_forest_model_prec = precision_score(y_test, random_forest_model_pred )
random_forest_model_recall = recall_score(y_test, random_forest_model_pred )
random_forest_model_roc = roc_auc_score(y_test, random_forest_model_pred )
random_forest_model_f1 = f1_score(y_test, random_forest_model_pred )
print(random_forest_model_acc)
print(random_forest_model_prec)
print(random_forest_model_recall)
print(random_forest_model_roc)
print(random_forest_model_f1)

TablarData = {'Methods': ['Logistic Regression', 'SVM', 'Random Forest', 'Decision Tree','KNN'],
        'Accuracy': [logistic_acc, svm_acc,random_forest_model_acc ,decision_tree_model_acc,knn_model_acc ],
        'Precision':[logistic_prec,svm_prec,random_forest_model_prec,decision_tree_model_prec,knn_model_prec],
        'Recall':[logistic_recall,svm_recall,random_forest_model_recall,decision_tree_model_recall,knn_model_recall],
        'F1-score':[logistic_f1,svm_f1,random_forest_model_f1,decision_tree_model_f1,knn_model_f1],
        'AUC score':[logistic_roc,svm_roc,random_forest_model_roc,decision_tree_model_roc,knn_model_roc]}

evaluation_metrics=pd.DataFrame(TablarData)

# Evaluation Metrics
evaluation_metrics

"""Perform 10-fold cross-validation and hyper-parameter tuning for all models"""

# Logistic regression - 10-fold cross-validation and hyper-parameter tuning

hyperparameter_set = {'C': [0.05,0.1,0.01,0.001,0.0001,0.5,0.08,0.7,0.47,0.8]}
from sklearn.model_selection import RandomizedSearchCV
logistic_cv=RandomizedSearchCV(logistic_model,hyperparameter_set, cv=10)
logistic_cv.fit(x_train_normalized,y_train)
logistic_predicted_cv=logistic_cv.predict(x_test_normalized)
logistic_cv.best_params_

logistic_acc_cv = accuracy_score(y_test, logistic_predicted_cv )
logistic_prec_cv = precision_score(y_test, logistic_predicted_cv )
logistic_recall_cv = recall_score(y_test, logistic_predicted_cv)
logistic_roc_cv = roc_auc_score(y_test, logistic_predicted_cv )
logistic_f1_cv = f1_score(y_test, logistic_predicted_cv)
print(logistic_acc_cv)
print(logistic_prec_cv)
print(logistic_recall_cv)
print(logistic_roc_cv)
print(logistic_f1_cv)

# Support Vector Machine - 10-fold cross-validation and hyper-parameter tuning

hyperparameter_set_svm = {'C': [0.001, 0.01, 0.1, 1, 10], 'kernel':['linear','rbf'], 'gamma':[0.001,0.01,0.1,1]}
svm=SVC(probability=True)
svm_cv=RandomizedSearchCV(svm,hyperparameter_set_svm,cv=10)
svm_cv.fit(x_train_normalized,y_train)
svm_predicted_cv=svm_cv.predict(x_test_normalized)
svm_cv.best_params_

svm_acc_cv = accuracy_score(y_test, svm_predicted_cv )
svm_prec_cv = precision_score(y_test, svm_predicted_cv )
svm_recall_cv = recall_score(y_test, svm_predicted_cv )
svm_roc_cv = roc_auc_score(y_test, svm_predicted_cv )
svm_f1_cv = f1_score(y_test, svm_predicted_cv )
print(svm_acc_cv)
print(svm_prec_cv)
print(svm_recall_cv)
print(svm_roc_cv)
print(svm_f1_cv)

# Random Forest - 10-fold cross-validation and hyper-parameter tuning

hyperparameter_set_rf = {'n_estimators': [100, 200, 300, 400], 'max_features': ['auto', 'sqrt']}
random_forest = RandomForestClassifier(random_state=60)
random_forest_cv=RandomizedSearchCV(random_forest,hyperparameter_set_rf,cv=10)
random_forest_cv.fit(x_train_normalized,y_train)
random_forest_predicted_cv=random_forest_cv.predict(x_test_normalized)
random_forest_cv.best_params_

random_forest_model_acc_cv = accuracy_score(y_test, random_forest_predicted_cv )
random_forest_model_prec_cv = precision_score(y_test, random_forest_predicted_cv )
random_forest_model_recall_cv = recall_score(y_test, random_forest_predicted_cv )
random_forest_model_roc_cv = roc_auc_score(y_test, random_forest_predicted_cv )
random_forest_model_f1_cv = f1_score(y_test, random_forest_predicted_cv )
print(random_forest_model_acc_cv)
print(random_forest_model_prec_cv)
print(random_forest_model_recall_cv)
print(random_forest_model_roc_cv)
print(random_forest_model_f1_cv)

# KNN - 10-fold cross-validation and hyper-parameter tuning
hyperparameter_set_knn = {'n_neighbors': [6, 3, 5, 7, 9]}
knn = KNeighborsClassifier()
knn_cv=RandomizedSearchCV(knn,hyperparameter_set_knn,cv=10)
knn_cv.fit(x_train_normalized,y_train)
knn_predicted_cv=knn_cv.predict(x_test_normalized)
knn_cv.best_params_

knn_acc_cv = accuracy_score(y_test, knn_predicted_cv )
knn_prec_cv = precision_score(y_test, knn_predicted_cv )
knn_recall_cv = recall_score(y_test, knn_predicted_cv )
knn_roc_cv = roc_auc_score(y_test, knn_predicted_cv )
knn_f1_cv = f1_score(y_test, knn_predicted_cv )

TablarData_cv = {'Methods': ['Logistic Regression', 'SVM', 'Random Forest','KNN'],
        'Accuracy': [logistic_acc_cv, svm_acc_cv,random_forest_model_acc_cv ,knn_acc_cv ],
        'Precision':[logistic_prec_cv,svm_prec_cv,random_forest_model_prec_cv,knn_prec_cv],
        'Recall':[logistic_recall_cv,svm_recall_cv,random_forest_model_recall_cv,knn_recall_cv],
        'F1-score':[logistic_f1_cv,svm_f1_cv,random_forest_model_f1_cv,knn_f1_cv],
        'AUC score':[logistic_roc_cv,svm_roc_cv,random_forest_model_roc_cv,knn_roc_cv]}

evaluation_metrics_cv=pd.DataFrame(TablarData_cv)

evaluation_metrics_cv

# model ensemble using the best models
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
eclf = VotingClassifier(
    estimators=[('lr', logistic_model), ('svm', svm), ('rf', random_forest_model),('knn',knn_model)],
    voting='hard')
for clf, label in zip([logistic_model, svm, random_forest, knn,eclf], ['Logistic Regression', 'svm', 'Random Forest', 'knn','Ensemble']):
    scores = cross_val_score(clf, x_train_normalized, y_train, scoring='accuracy', cv=5)
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

# feature importance analysis random forest

random_forest = RandomForestClassifier(n_estimators = 5, random_state=60)
random_forest.fit(x_train_normalized,y_train)
random_forest_importance = random_forest.feature_importances_
print(random_forest_importance)

import matplotlib.pyplot as plt
features=["Feature_1","Feature_2","Feature_3","Feature_4","Feature_5","Feature_6","Feature_7","Feature_8","Feature_9","Feature_10","Feature_11"]
pos = np.arange(len(features))                    
plt.barh(pos, random_forest_importance )
plt.yticks(pos, labels=features)
plt.show()