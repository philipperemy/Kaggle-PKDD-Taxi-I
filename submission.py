import evaluation as be
import pandas as pd
import numpy as np
from helpers import *

import json
from sklearn import ensemble
from sklearn import dummy
import time

# Load all the data files
train = load_train_file()
test = load_test_file()
sample = pd.read_csv('data/sampleSubmission.csv')
print 'reading sample done'

# Convert polyline string to list of lists using json. You can also use: ast.literal_eval
test['POLYLINE'] = test['POLYLINE'].apply(json.loads)
train['POLYLINE'] = train['POLYLINE'].apply(json.loads)

# Very crude way of generating some data here. I know lat is long and long is lat ;)
##### Crude method begins here
lat1 = []
long1 = []
lat2 = []
long2 = []
lat_final = []
long_final = []

for i in range(len(train)):
    try:
        lat1.append(train['POLYLINE'].values[i][0][0])
    except:
        lat1.append(-999)
    try:
        lat2.append(train['POLYLINE'].values[i][-2][0])
    except:
        lat2.append(-999)
    try:
        lat_final.append(train['POLYLINE'].values[i][-1][0])
    except:
        lat_final.append(-999)

    try:
        long1.append(train['POLYLINE'].values[i][0][1])
    except:
        long1.append(-999)
    try:
        long2.append(train['POLYLINE'].values[i][-2][1])
    except:
        long2.append(-999)
    try:
        long_final.append(train['POLYLINE'].values[i][-1][1])
    except:
        long_final.append(-999)


train['LAT1'] = lat1
train['LAT2'] = lat2
train['LATF'] = lat_final
train['LONG1'] = long1
train['LONG2'] = long2
train['LONGF'] = long_final

lat1 = []
long1 = []
lat2 = []
long2 = []

for i in range(len(test)):
    try:
        lat1.append(test['POLYLINE'].values[i][0][0])
    except:
        lat1.append(-999)
    try:
        lat2.append(test['POLYLINE'].values[i][-1][0])
    except:
        lat2.append(-999)

    try:
        long1.append(test['POLYLINE'].values[i][0][1])
    except:
        long1.append(-999)
    try:
        long2.append(test['POLYLINE'].values[i][-1][1])
    except:
        long2.append(-999)

test['LAT1'] = lat1
test['LAT2'] = lat2
test['LONG1'] = long1
test['LONG2'] = long2
##### Crude method ends here

# drop some training data that doesnt have end-points
train = train[train['LATF'] != -999]
train = train[train['LONGF'] != -999]

# drop columns for benchmark model
train = train.drop(['TRIP_ID', 'TIMESTAMP', 'POLYLINE'], axis = 1)
test = test.drop(['TRIP_ID', 'TIMESTAMP', 'POLYLINE'], axis = 1)

# factorize categorical columns in training set
for i in train.columns:
    if train[i].dtype == 'object':
        print i
        train[i] = pd.factorize(train[i])[0]

# factorize categorical columns in test set
for i in test.columns:
    if test[i].dtype == 'object':
        print i
        test[i] = pd.factorize(test[i])[0]

# fill all NaN values with -1
train = train.fillna(-1)
test = test.fillna(-1)

# Generate Labels and drop them from training set
labels = np.array(train[['LATF', 'LONGF']])
train = train.drop(['LATF', 'LONGF'], axis = 1)
train = np.array(train)
test = np.array(test)

train = train.astype(float)
test = test.astype(float)

# Initialize the famous Random Forest Regressor from scikit-learn
clf = ensemble.RandomForestRegressor(n_jobs=-1, n_estimators=100)
print 'starting training'
clf.fit(train, labels)
print 'training done'
preds = clf.predict(test)
print 'prediction done'

# Write predictions to file
sample['LATITUDE'] = preds[:,1]
sample['LONGITUDE'] = preds[:,0]
sample.to_csv('data/sampleSubmission-%s.csv' % int(time.time()), index = False)


dmregressor = dummy.DummyRegressor();
dmregressor.fit(train, labels);
preds2 = dmregressor.predict(test);

#sample2['LATITUDE'] = preds2[:,1]
#sample2['LONGITUDE'] = preds2[:,0]


#print be.destinationMiningEvaluation(sample)
