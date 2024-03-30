"""
    Josue Antonio
    DS 2500
    HW 2
    5/27 - Summer 1 2023
    challenger_part_A.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

STATIONS = 'stations.csv'
TEMPS = 'temp_1986.csv'
CANAVERAL_LAT = 28.397
CANAVERAL_LONG = -80.606
P = 1

# Python 3 program for the haversine formula
# Citation: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
def haversine(lat1, lon1, lat2, lon2):
    """
        Compute haversine distance between 2 gps locations
        lat_i, lon_i - gps locations (latitude, longitude)
        return haversine distance
    """
    d_lat = (lat2 - lat1) * np.pi / 180.0
    d_lon = (lon2 - lon1) * np.pi / 180.0

    lat1 = lat1 * np.pi / 180.0
    lat2 = lat2 * np.pi / 180.0

    a = (np.power(np.sin(d_lat / 2), 2) +
         np.power(np.sin(d_lon / 2), 2) *
         np.cos(lat1) * np.cos(lat2))
    rad = 6371
    c = 2 * np.arcsin(np.sqrt(a))
    return rad * c


def read_stations_data(filename, header):
    """
        Read a csv file into a dataframe, dropping rows with NaN values,
        and dropping rows with (0, 0) for (lat, long)
        filename - csv file
        header - header list for dataframe
        return - the dataframe
    """
    df = pd.read_csv(filename, header=None)
    df.columns = header
    df.replace(0, float('NaN'), inplace=True)
    df.dropna(subset=['StationID', 'Lat', 'Long'], inplace=True)
    return df

def read_temps_data(filename, header):
    """
        Read a csv file into a dataframe, dropping rows with NaN values
        filename - csv file
        header - header list for dataframe
        return - the dataframe
    """
    df = pd.read_csv(filename, header=None)
    df.columns = header
    df.dropna(subset=['StationID', 'Month', 'Day', 'Temp'], inplace=True)
    return df

def idw_interpolate(df, dist_col, temp_col):
    """
        Compute idw interpolation for every day of a given month
        and store result in a series
        df - dataframe,
        dist_col - name of distance column in dataframe
        temp_col - name of temp column in dataframe
        return - a series
    """
    df['inv_dist'] = 1 / (df[dist_col] ** P)
    df['weighted'] = df[temp_col] * df.inv_dist
    grouped = df.groupby('Day')
    result = grouped.weighted.sum() / grouped.inv_dist.sum()
    return result

def plot_temps(series, color):
    """
    Plot the result series at Canaveral for every day in Jan - 1986
    series - result series
    color - color of plot and text labels
    return - nothing
    """
    plt.figure(figsize=(7, 6), dpi=150)
    series.plot(color=color)
    plt.xticks([i for i in range(1, 32)], rotation=60)
    plt.text(series.idxmin() - 1.5, series.min() - 1, 'Jan ' + str(series.idxmin()) + 'th', fontsize=8, color=color)
    plt.title('Cape Canaveral Temperature (Jan-1986)', color=color)
    plt.xlabel('Day', color=color)
    plt.ylabel('Temperature (Fahrenheit)', color=color)
    plt.show()

def main():
    # Gather data - read data and store in dataframes
    stations_df = read_stations_data(STATIONS, ['StationID', 'WBAN', 'Lat', 'Long'])
    temps_df = read_temps_data(TEMPS, ['StationID', 'WBAN', 'Month', 'Day', 'Temp'])

    # Computation - filter stations that are within 100km from Canaveral using the
    # haversine distance formula; Store filtered rows
    stations_df['Canaveral_dist'] = stations_df.apply(lambda row:
                                haversine(CANAVERAL_LAT, CANAVERAL_LONG, row.Lat, row.Long), axis=1)
    close_stations = stations_df[stations_df.Canaveral_dist <= 100]

    # Merge stations df with temps df and filter by January entries
    merged = pd.merge(close_stations, temps_df, on='StationID')
    merged = merged[merged.Month == 1]

    # Estimate the temp at Cape Canaveral using inverse distance weighting interpolation
    result = idw_interpolate(merged, 'Canaveral_dist', 'Temp')

    # Communication - plot temp at Canaveral for every day of Jan 1986
    plot_temps(result, 'midnightblue')


if __name__ == "__main__":
    main()
