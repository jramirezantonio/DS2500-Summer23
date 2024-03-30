"""
    Josue Antonio
    DS 2500
    HW 2
    5/27 - Summer 1 2023
    challenger_part_B.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.colors import ListedColormap

STATIONS = 'stations.csv'
TEMPS = 'temp_1986.csv'
MIN_LAT, MAX_LAT = 25.0, 50.0
MIN_LONG, MAX_LONG = -125.0, -65.0

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

def temp_helper(temp):
    """
        Assigns rgb color based on temperature range
        temp - given temperature
        return - 3-valued color vector
    """
    if temp == -99:
        return [255, 255, 255]
    elif temp > 90:
        return [255, 51, 51]
    elif temp > 80:
        return [255, 102, 102]
    elif temp > 70:
        return [255, 128, 0]
    elif temp > 60:
        return [153, 153, 51]
    elif temp > 50:
        return [255, 178, 102]
    elif temp > 40:
        return [0, 0, 255]
    elif temp > 30:
        return [153, 255, 255]
    elif temp > 20:
        return [0, 102, 204]
    elif temp > 10:
        return [0, 0, 204]
    elif temp > 0:
        return [127, 0, 255]
    else:
        return [51, 0, 102]

def locations_to_coords(df, rows, cols):
    """
        Map gps locations to (x, y) coords storing respective temperature
        df - temps dataframe
        return - image array
    """
    im_arr = np.full((rows, cols), -99.0)
    for index, row in df.iterrows():
        x = int(rows - ((row.Lat - MIN_LAT) / (MAX_LAT - MIN_LAT)) * rows)
        y = int(((row.Long - MIN_LONG) / (MAX_LONG - MIN_LONG)) * cols)
        im_arr[x][y] = row.Temp
    return im_arr

def image_plot(df, month, day):
    """
        Plot np array as image plot for given day and month of 1986, and plot custom colorbar
        df - temps dataframe
        month - given month (int)
        day - given month (int)
        return - nothing
    """
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df = df.loc[(df.Month == month) & (df.Day == day)]
    im_arr = locations_to_coords(df, 100, 150)
    rows, cols = im_arr.shape
    color_arr = np.zeros((rows, cols, 3), dtype=int)

    for i in range(rows):
        for j in range(cols):
            color_arr[i][j] = temp_helper(im_arr[i][j])

    # Extra credit attempt - custom colormap to use in colorbar to then plot
    # Obtained this result with the help of ChatGPT
    colors = np.array([[127, 0, 255], [0, 0, 204], [0, 102, 204], [153, 255, 255], [0, 0, 255], [255, 178, 102],
                       [153, 153, 51], [255, 128, 0], [255, 102, 102]])
    intervals = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    # Normalize the intervals to range from 0 to 1
    normalized_intervals = np.array(intervals) / 90.0

    # Create a colormap from the colors and normalized intervals
    cmap = ListedColormap(colors / 255.0)
    norm = plt.Normalize(0, 1)

    # Create a scalar mappable object
    scalar_map = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar_map.set_array([])

    plt.figure(figsize=(7, 6), dpi=150)
    plt.imshow(color_arr)
    plt.xlabel('Y-axis')
    plt.ylabel('X-axis')
    cbar = plt.colorbar(scalar_map, ticks=normalized_intervals)
    cbar.ax.set_yticklabels(intervals)
    cbar.set_label('Color Bar')
    plt.title('Continental US Temperature on ' + str(months[month]) + '-' + str(day) + ' 1986')
    plt.ylim(110, -10)
    plt.xlim(-10, 160)
    plt.show()

    # Extra credit attempt - overlay map of continental US
    # map = Image.open('cont_us.png')
    # map = map.resize((150, 100)) - same size as color_arr
    # plt.imshow(map, zorder=1)
    # plt.imshow(color_arr, zorder=2) - lower zorder means plot first or 'under' the other plots
    # Couldn't get this to work even when trying to change opacity levels for both the map and temperatures
    # Rescaling original map image to im_arr size results in significant loss of image quality
def main():
    # Gather data - read data and store in dataframes
    stations_df = read_stations_data(STATIONS, ['StationID', 'WBAN', 'Lat', 'Long'])
    temps_df = read_temps_data(TEMPS, ['StationID', 'WBAN', 'Month', 'Day', 'Temp'])

    # Merge stations df with temps df and filter by latitude and longitude ranges
    temps = pd.merge(stations_df, temps_df, on='StationID')
    temps = temps.loc[(temps.Lat > MIN_LAT) & (temps.Lat < MAX_LAT) & (temps.Long > MIN_LONG)
                      & (temps.Long < MAX_LONG)]

    # Communication -  plot temperatures across continental US for Jan 28th and Feb 1st
    image_plot(temps, 1, 28)
    image_plot(temps, 2, 1)


if __name__ == "__main__":
    main()