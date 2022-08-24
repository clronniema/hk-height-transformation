
from pyproj import Transformer
from pyproj import CRS

from util.closest_stations import point_to_closest_stations_id
from util.read_stations import load_stations_csv_as_gdf


def transform_hk80_to_llh(lat, lon):
    epsg4326 = CRS.from_epsg(4326) # WGS1984
    epsg2326 = CRS.from_epsg(2326) # Hong Kong 1980 Grid
    transformer = Transformer.from_crs(epsg4326, epsg2326)
    # deliberate swapping of y and x
    nx,ny=transformer.transform(lat, lon) 
    return nx,ny


def transform_one_height_value(stations_gdf, lat, lon, height, to_hk80=True):
    # finding the 4 closest stations and add the mean height difference the input height value
    stations_kd_map = point_to_closest_stations_id(stations_gdf, lon, lat)
    stations_keys = [k for k,v in stations_kd_map]
    stns = stations_gdf.query('stn in @stations_keys')

    # New Northing and Easting or Lat Lon comes from the step before (7 parameters)
    if to_hk80:
        n_height = height + stns["hd"].mean()
    else:
        n_height = height - stns["hd"].mean()
    return n_height


def main():
    stations_gdf = load_stations_csv_as_gdf()
    
    # define lat lon height input
    lat = 22.285663
    lon = 114.215286
    height = 10.0
    
    new_x, new_y = transform_hk80_to_llh(lat, lon)
    new_height = transform_one_height_value(stations_gdf, lat, lon, height)
    print(f"Calculated HK80 Coordinates: {new_x}, {new_y}, {new_height}")


if __name__ == "__main__":
    main()