import pandas as pd
import geopandas as gpd


def __dms2lat(row):
    lat = float(row["lat_d"]) + float(row["lat_m"])/60 + float(row["lat_s"])/(60*60)
    return lat


def __dms2lon(row):
    lon = float(row["lon_d"]) + float(row["lon_m"])/60 + float(row["lon_s"])/(60*60)
    return lon


def load_stations_csv_as_gdf():
    # read file using pandas without header and convert it to dataframes (control_pts_heights.csv)
    names=["stn", "lat_d", "lat_m", "lat_s", "lon_d", "lon_m", "lon_s", "ell_h", "pd_h"]
    csv = pd.read_csv('data/control_pts_heights.csv', header=None, sep=" ").values
    df = pd.DataFrame(csv, columns=names)

    # calculate each station's height difference (hd) between the two heights
    df['lat'] = df.apply(__dms2lat, axis=1)
    df['lon'] = df.apply(__dms2lon, axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]))
    gdf["hd"] =  gdf["pd_h"] - gdf["ell_h"]
    return gdf
