"""
Traffic Jam feature

Track the overall traffic status on the road in a district, including the number of roads 
at different traffic jam levels in different time periods and different districts. 
Higher values mean heavier traffic.



Region 54 don't have traffic observations at all.


Hogjian Wang
6/6/2016
"""


from PathConfig import *
from Utilities import *
from re import match
import numpy as np
from os import listdir
from os.path import join




def getTrafficJam(train_or_test="train"):
    """
    Get traffic jam by day
    """
    if train_or_test == "train":
        DATA_FOLDER = join(TrainFolder, TrafficFolder)
    elif train_or_test == "test":
        DATA_FOLDER = join(TestFolder, TrafficFolder)
    else:
        print train_or_test
        raise NameError("Wrong train_or_test value!")
    traffic_files = listdir(DATA_FOLDER)

    DATE_TRAFFIC_MAP = {}
    for f in traffic_files:
        s = match(".*(\d{4}-\d{2}-\d{2}).*", f)
        date = s.groups()[0]

        print "Start processing {0}".format(date)
        with open(join(DATA_FOLDER, f), 'r') as fin:
            traffics = {}
            for line in fin:
                ls = line.strip().split("\t")
                time = ls[5]
                tid = getTimeSlotFromTimestamp(time, date)
                region_id = REGIONS[ls[0]]
                # ls[1] - ls[4] are road count in different congestion level
                s = map(lambda s: int(s[2:]), ls[1:5])
                if region_id not in traffics:
                    traffics[region_id] = {}
                if tid not in traffics[region_id]:
                    traffics[region_id][tid] = np.array(s)
                else:
                    print "More than one observations in one time slot."

            for region in traffics:
                traffic_TS = []
                for k in range(144):
                    if k in traffics[region]:
                        traffic_TS.append(traffics[region][k])
                    else:
                        if k == 0:
                            kn = nextAvailable(traffics[region], k)
                            traffic_TS.append(traffics[region][kn])
                        elif k == 143:
                            kp = previousAvailable(traffics[region], k)
                            traffic_TS.append(traffics[region][kp])
                        else:
                            kn = nextAvailable(traffics[region], k)
                            kp = previousAvailable(traffics[region], k)
                            traffic_TS.append( (traffics[region][kn] + traffics[region][kp]) / 2)
                traffics[region] = traffic_TS


        DATE_TRAFFIC_MAP[date] = traffics
    return DATE_TRAFFIC_MAP
                


def nextAvailable(ts, idx):
    while idx not in ts:
        idx += 1
    return idx


def previousAvailable(ts, idx):
    while idx not in ts:
        idx -= 1
    return idx


def printMissingRegion(s):
    """
    s is DATE_TRAFFIC_MAP
    """
    for day in s:
        print day
        for region in range(1, 67):
            if region not in s[day]:
                print region





def averageNumObservations(region_map):
    """
    Count average number of traffic observations in one day for one region.

    region_map
        is a map (region_id, list[observations])
    """
    c = map(len, region_map.values())
    return np.mean(c), np.sum(c)





if __name__ == "__main__":
    s = getTrafficJam()
    printMissingRegion(s)
    
    