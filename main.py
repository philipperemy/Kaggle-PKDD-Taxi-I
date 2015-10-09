import numpy as np
from helpers import *
import json
from sklearn import ensemble
#from sklearn import dummy
from serialize import *
import time

pre_process = 0

if pre_process:

    #process the files
    [lat1, long1, lat2, long2, lat_final, long_final] = pre_process_train_data()
    serialize(lat1, "lat1")
    serialize(long1, "long1")
    serialize(lat2, "lat2")
    serialize(long2, "long2")
    serialize(lat_final, "lat_final")
    serialize(long_final, "long_final")

    [lat1_t, long1_t, lat2_t, long2_t] = pre_process_test_data()
    serialize(lat1_t, "lat1_t")
    serialize(long1_t, "long1_t")
    serialize(lat2_t, "lat2_t")
    serialize(long2_t, "long2_t")

    print "Program will stop to clean memory"
    exit()

# Load all the data files
train = load_train_file()
test = load_test_file()

lat1 = unserialize("lat1")
long1 = unserialize("long1")
lat2 = unserialize("lat2")
long2 = unserialize("long2")
lat_final = unserialize("lat_final")
long_final = unserialize("long_final")

lat1_t = unserialize("lat1_t")
long1_t = unserialize("long1_t")
lat2_t = unserialize("lat2_t")
long2_t = unserialize("long2_t")

train['LAT1'] = lat1
train['LAT2'] = lat2
train['LATF'] = lat_final
train['LONG1'] = long1
train['LONG2'] = long2
train['LONGF'] = long_final

test['LAT1'] = lat1_t
test['LAT2'] = lat2_t
test['LONG1'] = long1_t
test['LONG2'] = long2_t

# drop some training data that doesnt have end-points
train = train[train['LATF'] != -999]
train = train[train['LONGF'] != -999]

# drop columns for benchmark model
print("drop columns"),
train = train.drop(['TRIP_ID', 'TIMESTAMP', 'POLYLINE'], axis = 1)
test = test.drop(['TRIP_ID', 'TIMESTAMP', 'POLYLINE'], axis = 1)
print " ... [OK]"


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
clf = ensemble.RandomForestRegressor(n_jobs=-1, n_estimators=2)
print 'starting training'
clf.fit(train, labels)
print 'training done'
preds = clf.predict(test)
print 'prediction done'

sample = pd.read_csv('data/sampleSubmission.csv')
sample['LATITUDE'] = preds[:,1]
sample['LONGITUDE'] = preds[:,0]
sample.to_csv('results/sampleSubmission-%s.csv' % int(time.time()), index = False)


#dmregressor = dummy.DummyRegressor();
#dmregressor.fit(train, labels);
#preds2 = dmregressor.predict(test);

#sample2['LATITUDE'] = preds2[:,1]
#sample2['LONGITUDE'] = preds2[:,0]


#print be.destinationMiningEvaluation(sample)
