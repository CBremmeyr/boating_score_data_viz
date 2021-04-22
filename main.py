# main.py
#
# Author: Corbin Bremmeyr
# Date: 21 April 2021
#
# CIS 320 Final Project: Best time for boating on lake Michigan
# Generate line graphs for each of the four weather measurments

import pandas as pd
import matplotlib.pyplot as plt

#
# Generate a line graph that has dates for the x-axis data
#
def time_line_plot(time, y_data, title, x_label, y_label):
    pd_time_data = pd.to_datetime(time)
    DF = pd.DataFrame()
    DF["value"] = y_data
    DF = DF.set_index(pd_time_data)
    plt.plot(DF)
    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

#
# Load dataset
#

print("Loading data...", end='')

time_data = []
weather_data = []
with open("holland_buoy_data.txt") as data_file:
    prev_date_str = None
    curr_date_str = None

    wind_speed_sum   = 0.0
    wave_height_sum  = 0.0
    air_temp_sum     = 0.0
    water_temp_sum   = 0.0

    wind_speed_len   = 0
    wave_height_len  = 0
    air_temp_len     = 0
    water_temp_len   = 0

    wind_speed_avg  = 0.0
    wave_height_avg = 0.0
    air_temp_avg    = 0.0
    water_temp_avg  = 0.0

    for line in data_file:

        # Ignore lines with unit information
        if line[0] == '#':
            continue

        # Make list of row values
        split_line = line.split()

        # Make date string for this line's data
        curr_date_str = split_line[0] + '/' + split_line[1] + '/' + split_line[2]

        # Check if this line is for a new day
        if curr_date_str != prev_date_str and prev_date_str != None:

            # Calculate averages for previous day
            wind_speed_avg  = wind_speed_sum  / wind_speed_len
            wave_height_avg = wave_height_sum / wave_height_len
            air_temp_avg    = air_temp_sum    / air_temp_len
            water_temp_avg  = water_temp_sum  / water_temp_len

            # Save previous days data
            time_data.append(curr_date_str)
            weather_data.append([wind_speed_avg, wave_height_avg, air_temp_avg, water_temp_avg])

            # Restart sum and len accumulators
            wind_speed_sum   = float(split_line[3])
            wave_height_sum  = float(split_line[4])
            air_temp_sum     = float(split_line[5])
            water_temp_sum   = float(split_line[6])
            wind_speed_len   = 1
            wave_height_len  = 1
            air_temp_len     = 1
            water_temp_len   = 1

        # Acculate new values into sum & len
        else:
            wind_speed_sum   += float(split_line[3])
            wave_height_sum  += float(split_line[4])
            air_temp_sum     += float(split_line[5])
            water_temp_sum   += float(split_line[5])

            wind_speed_len   += 1
            wave_height_len  += 1
            air_temp_len     += 1
            water_temp_len   += 1

        prev_date_str = curr_date_str

# Don't forget about the last list entry

# Calculate averages for previous day
wind_speed_avg  = wind_speed_sum  / wind_speed_len
wave_height_avg = wave_height_sum / wave_height_len
air_temp_avg    = air_temp_sum    / air_temp_len
water_temp_avg  = water_temp_sum  / water_temp_len

# Save previous days data
time_data.append(curr_date_str)
weather_data.append([wind_speed_avg, wave_height_avg, air_temp_avg, water_temp_avg])

print("done")

#
# Plot each data column vs time
#

# Get list for each weather data columns & dates
wind_speed_data  = []
wave_height_data = []
air_temp_data    = []
water_temp_data  = []
for row in weather_data:
    wind_speed_data.append(row[0])
    wave_height_data.append(row[1])
    air_temp_data.append(row[2])
    water_temp_data.append(row[3])

pd_time_data = pd.to_datetime(time_data)

# Plot wind speed data
time_line_plot(time_data, wind_speed_data, "Wind Speed", "Date", "Speed (m/s)")

# Plot wave height data
time_line_plot(time_data, wave_height_data, "Wave Height", "Date", "Height (m)")

# Plot air temperature data
time_line_plot(time_data, air_temp_data, "Air Temperature", "Date", "Temperature (°C)")

# Plot water temperature data
time_line_plot(time_data, water_temp_data, "Water Temperature", "Date", "Temperature (°C)")

#
# Generate score based on user set weights
#

# User set weights
# Bigger numbers indecate that the consideration of that metric is more important
# positive values if the value is perfered to be higher, negative if values are perfered to be smaller
# My personal values for dinghie sailboating
user_weights = [
        0.80,   # Wind speed
       -0.65,   # Wave height
        0.75,   # Air temp
        0.70,   # Water temp
        ]

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def scale_to_0_100(orig):
    orig_range = (min(orig), max(orig))
    scaled_list = []
    for i in orig:
        scaled_list.append(scale(i, orig_range, (0, 100)))
    return scaled_list

# Scale weather data values to range of 0 to 100
scaled_wind_speed  = scale_to_0_100(wind_speed_data)
scaled_wave_height = scale_to_0_100(wave_height_data)
scaled_air_temp    = scale_to_0_100(air_temp_data)
scaled_water_temp  = scale_to_0_100(water_temp_data)

# MAC weights and weather data
boating_score = []
for i in range(len(scaled_wind_speed)):
    mac = 0
    mac += user_weights[0] * scaled_wind_speed[i]
    mac += user_weights[1] * scaled_wave_height[i]
    mac += user_weights[2] * scaled_air_temp[i]
    mac += user_weights[3] * scaled_water_temp[i]
    boating_score.append(mac)

# Plot boating score on line graph
time_line_plot(time_data, boating_score, "Boating Score", "Date", "Score")

#time_line_plot(time_data, water_temp_data, "Water Temperature", "Date", "Temperature (°C)")
#def time_line_plot(time, y_data, title, x_label, y_label):
