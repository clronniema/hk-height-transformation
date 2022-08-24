import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def __points_distance(A, B):
    return A.distance(B)


def point_to_closest_stations_id(stations_gdf, lon, lat, num_of_closest_stations=4):
    if num_of_closest_stations <= 0:
        raise Exception("Number of closest station must be larger than 0")
    input = Point((lon, lat))
    station_distance = {}
    for _, row in stations_gdf.iterrows():
        # only suitable for small area
        station = row["geometry"]
        dist = __points_distance(input, station)
        station_distance[row["stn"]] = dist

    # find the 4 closest stations
    sorted_station_distances = sorted(station_distance.items(), key=lambda x:x[1])[0:num_of_closest_stations]
    return sorted_station_distances
