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




def calculateDemandSupplyGap(time_series_type="gap", train_or_test="test"):
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
                    ORDERS_MAP[region_id] = np.zeros(144)

                if time_series_type == "gap":
                    ORDERS_MAP[region_id][tid] += 1 if driver_id == "NULL" else 0
                elif time_series_type == "demand":
                    ORDERS_MAP[region_id][tid] += 1
                elif time_series_type == "supply":
                    ORDERS_MAP[region_id][tid] += 0 if driver_id == "NULL" else 1
                else:
                    print time_series_type
                    raise NameError("Wrong time series type!")
                
        DATE_ORDERS_MAP[f[-10:]] = ORDERS_MAP
    return DATE_ORDERS_MAP




if __name__ == '__main__':
    import sys
    TS_TYPE = sys.argv[1]
    r = calculateDemandSupplyGap(TS_TYPE)
    import pickle
    pickle.dump(r, open("ORDERS_{0}".format(TS_TYPE), 'w'))
