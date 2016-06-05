"""
Build POI feature

Hongjian Wang
6/4/2016
"""

from PathConfig import *
from Utilities import *
from re import match
import numpy as np



# A global variables to track the POI category
POI_1st_category = None



def insertPOIEntry(POIs, region_id, POI_first_cat, count):
	"""
	Insert the first level POI category counts into the POIs map
	"""
	if region_id in POIs:
		if POI_first_cat in POIs[region_id]:
			POIs[region_id][POI_first_cat] += count
		else:
			POIs[region_id][POI_first_cat] = count
	else:
		POIs[region_id] = {}
		POIs[region_id][POI_first_cat] = count




def getPOIFeatureMatrix():
	"""
	Generate POI feature matrix for all regions.
	"""
	c = 0
	POIs = {}

	with open(POIdata, "r") as fin:
		for line in fin:
			c += 1
			ls = line.strip().split("\t")
			rid = REGIONS[ls[0]]
			pois = ls[1:]

			try: 
				for poi in pois:
					s = match("(\d+)#(\d+):(\d+)", poi)
					s = s.groups()
					insertPOIEntry(POIs, rid, s[0], int(s[2]))
			except AttributeError:
				"""
				Some POI entry does not have the second level category information.
				Namely, instead of "23#23:2000", the format is "12:234".
				"""
				s = match("(\d+):(\d+)", poi)
				s = s.groups()
				insertPOIEntry(POIs, rid, s[0], int(s[1]))

	# merge 1st level category
	POI_1st_category = list(reduce(set.union, map(set, map(dict.keys, POIs.values()))))

	POI_features = []
	for rid in range(1:NUMBER_REGIONS+1):
		counts = []
		for poi in POI_1st_category:
			counts.append(POIs[rid][poi] if poi in POIs[rid] else 0)
		POI_features.append(counts)


	POI_feature_matrix = np.array(POI_features)
	return POI_feature_matrix



POI_feature_matrix = getPOIFeatureMatrix()



