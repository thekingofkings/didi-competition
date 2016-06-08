"""
Calculate supply-demand gap



Hongjian Wang
6/4/2016
"""

from PathConfig import *
from Utilities import *

from os import listdir
from os.path import join
import numpy as np
import re




def calculateDemandSupplyGap(time_series_type="gap", train_or_test="train"):
    """
    Return a nested map.
    First level is DATE -> second_level_map.
    Second level is REGION_ID -> ORDERS.
    """
    if train_or_test == "train":
        DATA_FOLDER = join(TrainFolder, OrderFolder)
    elif train_or_test == "test":
        DATA_FOLDER = join(TestFolder, OrderFolder)
    else:
        print train_or_test
        raise NameError("Wrong train_or_test value!")
    order_files = listdir(DATA_FOLDER)



    DATE_ORDERS_MAP = {}
    for f in order_files:
        s = re.match(".*(\d{4}-\d{2}-\d{2}).*", f)
        date = s.groups()[0]
        print "Start processing {0}".format(date)
        with open(join(DATA_FOLDER, f), 'r') as fin:
            # (region_id -> demand-supply gap time series in one day)
            ORDERS_MAP = {}
            for line in fin:
                ls = line.strip().split("\t")
                driver_id = ls[1]
                region_id = REGIONS[ls[3]]
                time = ls[6]
                tid = getTimeSlotFromTimestamp(time, date)

                if region_id not in ORDERS_MAP:
                    ORDERS_MAP[region_id] = np.ones(144) * -1

                if time_series_type == "gap":
                    ORDERS_MAP[region_id][tid] += 1 if driver_id == "NULL" else 0
                elif time_series_type == "demand":
                    ORDERS_MAP[region_id][tid] += 1
                elif time_series_type == "supply":
                    ORDERS_MAP[region_id][tid] += 0 if driver_id == "NULL" else 1
                else:
                    print time_series_type
                    raise NameError("Wrong time series type!")
        
        for region in ORDERS_MAP:
            ORDERS_MAP[region] = map(lambda x: x+1 if x != -1 else x, ORDERS_MAP[region])
        DATE_ORDERS_MAP[date] = ORDERS_MAP
    return DATE_ORDERS_MAP





def weeklyPatternByRegion(DATE_ORDERS_MAP):
    """
    Calculate weekly average for different regions.
    """
    weekly_orders = [ {} for i in range(7) ]
    weekly_orders_cnt = np.zeros(7)
    for date in DATE_ORDERS_MAP:
        wd = getWeekDay(date)   # weekday has value 0 - 6 (Mon - Sun)
        weekly_orders[wd] = sumValue_2dicts(DATE_ORDERS_MAP[date], weekly_orders[wd])
        weekly_orders_cnt[wd] += 1.0

    for idx, cnt in enumerate(weekly_orders_cnt):
        for region in weekly_orders[idx]:
            weekly_orders[idx][region] /= cnt

    return weekly_orders






if __name__ == '__main__':
    import sys
    TS_TYPE = sys.argv[1]
    r = calculateDemandSupplyGap(TS_TYPE)
    import pickle
    pickle.dump(r, open("ORDERS_{0}".format(TS_TYPE), 'w'))
