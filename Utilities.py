"""
Utility functions

1) create district map (hashstring -> int_id)
2) deal with time

Expose the following global variables:
    REGIONS - a map of regions' id
    NUMBER_REGIONS - the number of regions in total

Hongjian
6/4/2016
"""

from PathConfig import *
import numpy as np


def getRegionMap():
    regions = {}
    with open(ClusterMap, "r") as fin:
        for line in fin:
            ls = line.strip().split("\t")
            regions[ls[0]] = int(ls[1])
    return regions



REGIONS = getRegionMap()
NUMBER_REGIONS = len(REGIONS)



def getTimeSlotFromTimestamp(timestr, date = None):
    """
    Get the index of 10-min time slot from a raw time string
    """
    ts = timestr.split(" ")
    if date and ts[0] == date:
        time = ts[1].split(":")
        mins = int(time[0]) * 60 + int(time[1])
        return mins / 10
    else:
        return -1



def getWeekDay(date):
    """
    Return weekday from date string.
    Monday is 0, Sunday is 6.
    """
    from datetime import datetime
    t = datetime.strptime(date, "%Y-%m-%d")
    return t.weekday()


def sumValue_2dicts(d1, d2):
    """
    Two dictionaries d1 and d2 has same set of keys.
    The values have type np.array.
    This function sum two dictionaries together.

    d1 is always full.
    d2 could be empty.
    """
    for k in d1:
        if k in d2:
            d1[k] = d1[k] + d2[k]
    return d1




def MAPE(grnd_truth, estimation):
    """
    Cacluate Mean Absolute Percentage Error
    """
    T = np.array(grnd_truth)
    E = np.array(estimation)
    return np.mean(np.abs(T-E) / T)
