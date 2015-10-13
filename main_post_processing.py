from helpers import *
from sklearn import ensemble
from serialize import *
import time
from constants import *

# Load all the data files
train = load_train_file()
test = load_test_file()

train['LAT1'] = unserialize("lat1")
train['LAT2'] = unserialize("lat2")
train['LONG1'] = unserialize("long1")
train['LONG2'] = unserialize("long2")
train['HOUR'] = unserialize("hours")
train[DURATION] = unserialize("duration")
train[SPEED] = unserialize("speed")
train[LAST_SPEED] = unserialize("last_speed")
train[LAST_LAST_SPEED] = unserialize("last_last_speed")

train['LATF'] = unserialize("lat_final")
train['LONGF'] = unserialize("long_final")

test['LAT1'] = unserialize("lat1_t")
test['LAT2'] = unserialize("lat2_t")
test['LONG1'] = unserialize("long1_t")
test['LONG2'] = unserialize("long2_t")
test['HOUR'] = unserialize("hours_t")
test[DURATION] = unserialize("duration_t")
test[SPEED] = unserialize("speed_t")
test[LAST_SPEED] = unserialize("last_speed_t")
test[LAST_LAST_SPEED] = unserialize("last_last_speed_t")

train.to_csv("debug/debug_train_before_cleaning.csv")
test.to_csv("debug/debug_test_before_cleaning.csv")

# drop lines with missing data for training set or suspicious lines
# drop some training data that doesn't have end-points
# Speed limit on highway is 120 in Portugal. However some drivers may drive a little bit faster. A value of 1000 should be discarded however.
print "remove lines when: missing data, speed is too high or 0, travel is too long, no end-points",
train = train[train[MISSING_DATA] != 1]

train = train[train[SPEED] < MAX_SPEED_LIMIT_BEFORE_DISCARDING]
train = train[train[SPEED] > 0] #speed must be positive

train = train[train[LAST_SPEED] < MAX_SPEED_LIMIT_BEFORE_DISCARDING]
train = train[train[LAST_SPEED] > 0] #speed must be positive

train = train[train['LATF'] != NA_VALUE]
train = train[train['LONGF'] != NA_VALUE]
print " ... [OK]"

test_duration = test.copy()
test_duration = test_duration.loc[test_duration["DURATION"] > 3300]

# drop columns for benchmark model
print "drop columns",
train = drop_useless_columns(train)
test = drop_useless_columns(test)
print " ... [OK]"

print "factorize",
factorize(train, test)
print " ... [OK]"

print "fill N/A with " + str(NA_VALUE),
train = train.fillna(NA_VALUE)
test = test.fillna(NA_VALUE)
print " ... [OK]"

print "generate labels and drop them from training set",
labels = np.array(train[['LATF', 'LONGF']])
train = train.drop(['LATF', 'LONGF'], axis = 1)
print "... [OK]"

train.to_csv("debug/debug_train_after_cleaning.csv")
test.to_csv("debug/debug_test_after_cleaning.csv")

# drop trip ids for benchmark model
print "drop trip ids",
train = drop_trip_ids(train)
test = drop_trip_ids(test)
print " ... [OK]"

#Random Forest is invariant to monotonic transformations of individual features. No need to normalize the values
print "convert sets to floating values",
train = np.array(train)
test = np.array(test)
train = train.astype(float)
test = test.astype(float)
print "... [OK]"

print "learning process"
clf = ensemble.RandomForestRegressor(n_jobs=-1, n_estimators=1, verbose = 1)
clf.fit(train, labels)
print " ... [OK]"

print "predict process"
predictions = clf.predict(test)
print " ... [OK]"

publish_file = 'results/sampleSubmission-%s.csv' % int(time.time())
print "publishing to file " + publish_file,
sample = pd.read_csv('data/sampleSubmission.csv')
sample['LATITUDE'] = predictions[:,1]
sample['LONGITUDE'] = predictions[:,0]

for trip_id in sample['TRIP_ID']:
    cond = test_duration["TRIP_ID"] == trip_id
    if sum(cond) == 1:
        lat1 = test_duration[cond]["LAT1"]
        long1 = test_duration[cond]["LONG1"]
        sample.loc[sample['TRIP_ID'] == trip_id,'LATITUDE'] = long1
        sample.loc[sample['TRIP_ID'] == trip_id,'LONGITUDE'] = lat1

sample.to_csv(publish_file, index = False)