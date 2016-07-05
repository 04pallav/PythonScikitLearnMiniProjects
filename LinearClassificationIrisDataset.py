
# coding: utf-8

# # Using a linear classifier to classify Iris Dataset

# In[1]:

get_ipython().magic('pylab inline')


# Import scikit-learn, numpy and pyplot

# In[2]:

import sklearn as sk
import numpy as np
import matplotlib.pyplot as plt


# Load Iris dataset

# In[3]:

from sklearn import datasets
iris = datasets.load_iris()
X_iris, y_iris = iris.data, iris.target
print X_iris.shape, y_iris.shape
print X_iris[0], y_iris[0]


# Create training and testing partitions and standarize data.

# In[4]:

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

# Get dataset with only the first two attributes
X, y = X_iris[:,:2], y_iris
# Split the dataset into a trainig and a testing set
# Test set will be the 25% taken randomly
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
print X_train.shape, y_train.shape
# Standarize the features
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)



# Plot the training data.

# In[5]:


colors = ['red', 'greenyellow', 'blue']
for i in xrange(len(colors)):
    px = X_train[:, 0][y_train == i]
    py = X_train[:, 1][y_train == i]
    plt.scatter(px, py, c=colors[i])

plt.legend(iris.target_names)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')


# Fit a Linear Classification method.

# In[6]:

# create the linear model classifier
from sklearn.linear_model import SGDClassifier
clf = SGDClassifier()
# fit (train) the classifier
clf.fit(X_train, y_train)
# print learned coeficients
print clf.coef_
print clf.intercept_


# Plot the three decision curves. Note that Class 0 is linearly separable, while Class 1 and Class 2 are not

# In[7]:

x_min, x_max = X_train[:, 0].min() - .5, X_train[:, 0].max() + .5
y_min, y_max = X_train[:, 1].min() - .5, X_train[:, 1].max() + .5
xs = np.arange(x_min,x_max,0.5)
fig, axes = plt.subplots(1,3)
fig.set_size_inches(10,6)
for i in [0,1,2]:
    axes[i].set_aspect('equal')
    axes[i].set_title('Class ' + str(i) + ' versus the rest')
    axes[i].set_xlabel('Sepal length')
    axes[i].set_ylabel('Sepal width')
    axes[i].set_xlim(x_min, x_max)
    axes[i].set_ylim(y_min, y_max)
    sca(axes[i])
    for j in xrange(len(colors)):
        px = X_train[:, 0][y_train == j]
        py = X_train[:, 1][y_train == j]
        plt.scatter(px, py, c=colors[j])
    ys = (-clf.intercept_[i]-xs*clf.coef_[i,0])/clf.coef_[i,1]
    plt.plot(xs,ys,hold=True)
    


# Evaluate a particular instance

# In[8]:


print clf.predict(scaler.transform([[4.7, 3.1]]))
print clf.decision_function(scaler.transform([[4.7, 3.1]]))


# Measure accuracy on the training set

# In[9]:

from sklearn import metrics
y_train_pred = clf.predict(X_train)
print metrics.accuracy_score(y_train, y_train_pred)


# Measure  accuracy on the testing set

# In[10]:

y_pred = clf.predict(X_test)
print metrics.accuracy_score(y_test, y_pred)


# Evaluate results using Precision, Recall and F-score, and show the confusion matrix

# In[11]:

print metrics.classification_report(y_test, y_pred, target_names=iris.target_names)
print metrics.confusion_matrix(y_test, y_pred)


# Create a new classifier: a pipeline of the standarizer and the linear model. Measure the cross-validation accuracy.

# In[12]:

from sklearn.cross_validation import cross_val_score, KFold
from sklearn.pipeline import Pipeline

# create a composite estimator made by a pipeline of the standarization and the linear model
clf = Pipeline([
        ('scaler', StandardScaler()),
        ('linear_model', SGDClassifier())
])
# create a k-fold croos validation iterator of k=5 folds
cv = KFold(X.shape[0], 5, shuffle=True, random_state=33)
# by default the score used is the one returned by score method of the estimator (accuracy)
scores = cross_val_score(clf, X, y, cv=cv)
print scores



# Calculate the mean and standard error of cross-validation accuracy

# In[13]:

from scipy.stats import sem

def mean_score(scores):
    """Print the empirical mean score and standard error of the mean."""
    return ("Mean score: {0:.3f} (+/-{1:.3f})").format(
        np.mean(scores), sem(scores))

print mean_score(scores)


# In[13]:



