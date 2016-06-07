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