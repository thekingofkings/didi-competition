"""
Calculate Weather feature

The weather features have three dimensions, which are 
weather (categorical), temperature, and PM2.5. 


Hongjian Wang
6/4/2016
"""


from PathConfig import *
from Utilities import *
from re import match
import numpy as np
from os import listdir
from os.path import join



def getWeather(train_or_test="train"):
    """
    Get weather vector by day
    """
    if train_or_test == "train":
        DATA_FOLDER = join(TrainFolder, WeatherFolder)
    elif train_or_test == "test":
        DATA_FOLDER = join(TestFolder, WeatherFolder)
    else:
        print train_or_test
        raise NameError("Wrong train_or_test value!")
    weather_files = listdir(DATA_FOLDER)
    

    DATE_WEATHER_MAP = {}
    for f in weather_files:
        s = match(".*(\d{4}-\d{2}-\d{2}).*", f)
        date = s.groups()[0]

        print "Start processing {0}".format(date)
        with open(join(DATA_FOLDER, f), 'r') as fin:
            weathers = {}
            for line in fin:
                ls = line.strip().split("\t")
                time = ls[0]
                # weather features have three dimensions
                weather = np.array( [float(ls[1]), float(ls[2]), float(ls[3]), 1.0] )
                tid = getTimeSlotFromTimestamp(time, date)
                if tid not in weathers:
                    weathers[tid] = weather
                else:
                    # each time slot may have multiple observations
                    weathers[tid] += weather

        WEATHER_MATRIX = []
        # some time slot may not have weather observations
        missing_time_slot = []
        # calculate average for each time slot
        for k in range(144):
            if k in weathers:
                weather_feature = weathers[k][0:3] / weathers[k][3]
                WEATHER_MATRIX.append(weather_feature)
            else:
                missing_time_slot.append(k)
                WEATHER_MATRIX.append(np.zeros(3))

        # interploate the missing weather features
        for k in missing_time_slot:
            if k == 0:
                WEATHER_MATRIX[k] = WEATHER_MATRIX[k+1]
            elif k == 143:
                WEATHER_MATRIX[k] = WEATHER_MATRIX[k-1]
            else:
                WEATHER_MATRIX[k] = (WEATHER_MATRIX[k+1] + WEATHER_MATRIX[k-1]) / 2


        WEATHER_MATRIX = np.array(WEATHER_MATRIX)

        DATE_WEATHER_MAP[date] = WEATHER_MATRIX

    return DATE_WEATHER_MAP



if __name__ == "__main__":
    s = getWeather()
    for k in s:
        assert s[k].shape == (144, 3)

