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




def calculateDemandSupplyGap():
	"""
	Return a nested map.
	First level is DATE -> second_level_map.
	Second level is REGION_ID -> ORDERS.
	"""
	DATA_FOLDER = join(TrainFolder, OrderFolder)
	order_files = listdir(DATA_FOLDER)



	DATE_ORDERS_MAP = {}
	for f in order_files:
		print "Start processing {0}".format(f[-10:])
		with open(join(DATA_FOLDER, f), 'r') as fin:
			# (region_id -> demand-supply gap time series in one day)
			ORDERS_MAP = {}
			for line in fin:
				ls = line.strip().split("\t")
				driver_id = ls[1]
				region_id = REGIONS[ls[3]]
				time = ls[6]
				tid = getTimeSlotFromTimestamp(time, f[-10:])

				if region_id not in ORDERS_MAP:
					ORDERS_MAP[region_id] = np.zeros(144)

				ORDERS_MAP[region_id][tid] += 1 if driver_id == "NULL" else -1
				
		DATE_ORDERS_MAP[f[-10:]] = ORDERS_MAP