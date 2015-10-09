import pandas as pd
import json

#
# File Import
#

TRAIN_CSV_FILE_NAME = "data/train.csv"
TEST_CSV_FILE_NAME = "data/test.csv"

def load_train_file():
    print 'reading train file',
    handle = load_file(TRAIN_CSV_FILE_NAME)
    print ' ... [OK]'
    return handle


def load_test_file():
    print 'reading test file',
    handle = load_file(TEST_CSV_FILE_NAME)
    print ' ... [OK]'
    return handle


def load_file(str):
    handle = pd.read_csv(str)
    return handle


#
# File Processing
#
def new_data_frame():
    return pd.DataFrame()


def process_test_data(test):
    test['POLYLINE'] = test['POLYLINE'].apply(json.loads)
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
    test = test.drop(['TRIP_ID', 'TIMESTAMP', 'POLYLINE'], axis = 1)
    return test


def pre_process_train_data():

    #
    # read file chunk by chunk as file is really big. processing will be much faster.
    #
    lat1 = []
    long1 = []
    lat2 = []
    long2 = []
    lat_final = []
    long_final = []

    count = 1
    chunksize = 10 ** 5
    for train in pd.read_csv(TRAIN_CSV_FILE_NAME, chunksize=chunksize):
        train['POLYLINE'] = train['POLYLINE'].apply(json.loads)
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

            count += 1
            if count % 1000 == 0:
                print count

    return lat1, long1, lat2, long2, lat_final, long_final


def pre_process_test_data():
    test = pd.read_csv(TEST_CSV_FILE_NAME)
    test['POLYLINE'] = test['POLYLINE'].apply(json.loads)

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

    return lat1, long1, lat2, long2