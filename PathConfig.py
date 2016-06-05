"""
The path configurations of raw data


Hongjian
6/4/2016
"""

TestFolder = "/Users/hongjianw/Documents/season_1/test_set_1"
TrainFolder = "/Users/hongjianw/Documents/season_1/training_data"


# Cluster map and POI data are 
#  1) static over time
#  2) exactly the same from training to testing
ClusterMap = TrainFolder + "/cluster_map/cluster_map"
POIdata = TrainFolder + "/poi_data/poi_data"


OrderFolder = "order_data"
TrafficFolder = "traffic_data"
WeatherFolder = "weather_data"
