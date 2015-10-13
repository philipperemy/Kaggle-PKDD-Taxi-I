import pandas as pd
import json
import speed as sp
from datetime import datetime
import numpy as np
from constants import *
import copy as cp


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


# File Processing
def new_data_frame():
    return pd.DataFrame()


def pre_process_generic_data(filename, isTest = False):

    lat1 = []; long1 = []; lat2 = []; long2 = []; lat_final = []; long_final = [];
    hours = []; duration = []; mean_speed = []; last_speed = []; last_last_speed = []

    count = 1
    chunk_size = 10 ** 5 # 10^5 = 100.000 lines at a time
    for data in pd.read_csv(filename, chunksize = chunk_size):
        data[POLYLINE] = data[POLYLINE].apply(json.loads)
        for i in range(len(data)):

            datetime_tokyo = datetime.fromtimestamp(data[TIMESTAMP].values[i])
            hours.append(datetime_tokyo.hour - UTC_LAG_BETWEEN_TOKYO_AND_LISBON)

            #reminder: the last value should not be known from the training set. Better known as lat_final
            polyline = data[POLYLINE].values[i]
            duration.append( len(polyline) * 15)

            if len(polyline) > 1:

                if isTest:
                    polyline_tmp = polyline # pointer to polyline. No problem. It's Read Only
                else:
                    polyline_tmp = cp.copy(polyline)
                    polyline_tmp.pop()

                speeds = sp.speeds(polyline_tmp)
                mean_speed.append(np.mean(speeds))
                last_speed.append(speeds[-1])

                if len(speeds) > 1:
                    last_last_speed.append(speeds[-2]) #two last speeds to have an acceleration measure
                else:
                    last_last_speed.append(0)
            else:
                mean_speed.append(0)
                last_speed.append(0)
                last_last_speed.append(0)

            if isTest:
                append_to_list(lat1, polyline, 0, LAT_ID)
                append_to_list(lat2, polyline, -1, LAT_ID)
                append_to_list(long1, polyline, 0, LONG_ID)
                append_to_list(long2, polyline, -1, LONG_ID)

            else:
                append_to_list(lat1, polyline, 0, LAT_ID)
                append_to_list(lat2, polyline, -2, LAT_ID)
                append_to_list(lat_final, polyline, -1, LAT_ID)
                append_to_list(long1, polyline, 0, LONG_ID)
                append_to_list(long2, polyline, -2, LONG_ID)
                append_to_list(long_final, polyline, -1, LONG_ID)

            count += 1
            if count % 1000 == 0:
                print count

    if isTest :
        return lat1, long1, lat2, long2, hours, duration, mean_speed, last_speed, last_last_speed
    else:
        return lat1, long1, lat2, long2, lat_final, long_final, hours, duration, mean_speed, last_speed, last_last_speed


def pre_process_train_data():
    return pre_process_generic_data(TRAIN_CSV_FILE_NAME, isTest = False)


def pre_process_test_data():
    return pre_process_generic_data(TEST_CSV_FILE_NAME, isTest = True)

#jointly factorize to have the same values for the factors
def factorize(train, test):
    joint_factorize(train, test, TAXI_ID)
    joint_factorize(train, test, ORIGIN_CALL)
    joint_factorize(train, test, ORIGIN_STAND)
    joint_factorize(train, test, DAY_TYPE)
    joint_factorize(train, test, CALL_TYPE)


def joint_factorize(train, test, column_name):
    joint_factors = pd.factorize(list(train[column_name]) + list(test[column_name]))
    train_length = len(train[column_name])
    range_train = range(train_length)
    train[column_name] = joint_factors[0][range_train]
    range_test = range(train_length,len(joint_factors[0]))
    test[column_name] = joint_factors[0][range_test]



def drop_useless_columns(data_set):
    data_set = data_set.drop([POLYLINE, MISSING_DATA, TIMESTAMP], axis = 1)
    return data_set


#not at the same time for debugging purposes
def drop_trip_ids(data_set):
    data_set = data_set.drop([TRIP_ID], axis = 1)
    return data_set


def append_to_list(list, polyline, i, j):
    try:
        list.append(polyline[i][j])
    except:
        list.append(NA_VALUE)