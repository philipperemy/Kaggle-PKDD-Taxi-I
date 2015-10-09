__author__ = 'Philippe'

from math import pi
from math import sqrt

import numpy as np

def HaversineDistance(lat1,lon1,lat2,lon2):
    REarth = 6371
    lat = np.absolute(lat1-lat2)*pi/180
    lon = np.absolute(lon1-lon2)*pi/180
    lat1 = lat1*pi/180
    lat2 = lat2*pi/180
    a = np.sin(lat/2)*np.sin(lat/2)+np.cos(lat1)*np.cos(lat2)*np.sin(lon/2)*np.sin(lon/2)
    d = 2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
    d = REarth*d
    return(d)

def RMSE(pre,real):
    return(sqrt(np.mean((pre-real)*(pre-real))))

def meanHaversineDistance(lat1,lon1,lat2,lon2):
    return(np.mean(HaversineDistance(lat1,lon1,lat2,lon2)))


def travelTimePredictionEvaluation(submission,answers):
    return (RMSE(submission,answers))

def destinationMiningEvaluation(submission,answers):
    lat_sub = submission['LATITUDE']
    lon_sub = submission['LONGITUDE']

    lat_real = answers['LATITUDE']
    lon_real = answers['LONGITUDE']
    return (meanHaversineDistance(lat_sub,lon_sub,lat_real,lon_real))