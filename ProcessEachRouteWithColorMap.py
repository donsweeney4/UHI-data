"""
This script processes each route file in the input directory and creates a color-coded map of the route with temperature data.


"""
import pandas as pd
import numpy as np
import folium
import sys
import os
import math
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import branca.colormap as cm
from MyRemoteSQL import sql_connection

"""
Properties of the pandas dataframes used in this script:

df_step1 =  Data after removal of rows with missing data 
            df.dropna(subset=['rtcTime', 'gps_Lat', 'gps_Long', 'degC', 'gps_GroundSpeed'])

df_step2 = Remove rows with speed below specified speed in MPH in parameters.py 
            df_step1[df_step1['gps_GroundSpeed'] >= 4470.4]  # 4470.4 mm/sec is equivalent to 10 mph

df_step3 =  set the sample time window

df_step4 =  adjust temperature drift (temperatue slope) over time

df_step5 =  [SAVED FILE] concatenate all dataframes over the time window and correct temperature SAVED as .csv file
            pd.concat([df_step4, df_step3)

df_step6 =  concatenate all dataframes for the entire run

df_step7 =  [SAVED FILE] same as df_step5 but with reduced columns -> gps_Lat, gps_Long, corrected_temperature, SourceFile 


 """  


def validate_and_convert(row):
    try:
        # Validate and convert latitude, longitude
        latitude = float(row['gps_Lat']) * 1e-7
        longitude = float(row['gps_Long']) * 1e-7
        groundspeed = float(row['gps_GroundSpeed']) 
        
        
        if latitude is None or longitude is None:
            print(f"Skipping row with invalid latitude or longitude: {row}")


        return latitude, longitude, groundspeed
    except ValueError as e:
        print(f"Error processing row {row}: {e}", file=sys.stderr)
        return None, None, None

##########################################################################################
#####################   Main_process  ##################################################
##########################################################################################

def main_process(input_directory):

##########################################################################################
##################### Input Parameters ##################################################
##########################################################################################

    
    # Dynamically add input_directory to sys.path
    sys.path.append(input_directory)
    import parameters as p

# Define the time window for the data
    input_directory = p.input_directory # Replace with your directory path
    output_directory = p.output_directory # Replace with your directory path
    start_time = p.start_time
    end_time =  p.end_time
    cuttoff_speed_MPH = p.cuttoff_speed_MPH 
    temperature_drift = p.temperature_drift   #  Adjust temperature drift over time  
    color_coded_temperature_map =  p.color_coded_temperature_map
    color_coded_route_map =  p.color_coded_route_map
    temperature_map_TimeWindow =  p.temperature_map_TimeWindow
    temperature_map_entireTime = p.temperature_map_entireTime
    solid_color_by_route = p.solid_color_by_route
    color_table_min = p.color_table_min
    color_table_max = p.color_table_max
    combined_data =  p.combined_data
    combined_data_reduced_columns =  p.combined_data_reduced_columns
 
##########################################################################################
##########################################################################################
##########################################################################################

# Simple conversion of speed from MPH to mm/sec
    cuttoff_speed = cuttoff_speed_MPH * 447.04 # convert MPH to mm/sec
    os.makedirs(output_directory, exist_ok=True)
    timestamp_start = pd.to_datetime(start_time)
    timestamp_end = pd.to_datetime(end_time)
    solid_color_list = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']
    ##########################################################################################




    directory = input_directory  # directory path input parameters and input data files
    df_list = []
    center_lat, center_lon = 37.6819, -121.7680

    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)
    m2= folium.Map(location=[center_lat, center_lon], zoom_start=18)
    
    i = 0

    # DataFrame to hold all temperature vs. time data
    df_step5 = pd.DataFrame()
    df_step6 = pd.DataFrame()
    df_step7 = pd.DataFrame()

    

    print(f"\n There are {len(os.listdir(directory))} files in the directory {directory}")
    for filename in os.listdir(directory):
        if filename.endswith(".TXT"):   
            print(f"\n\n ================================") 
            print(f"\n Processing file {filename}") 
            i += 1  # Increment the .TXT file index number
            file_path = os.path.join(directory, filename)

            # Read the CSV file
            try:
                df = pd.read_csv(file_path)
                df.loc[:,'SourceFile'] = filename  # Add a column to indicate the source file

                print(f"\n\n  ======================== \n  File {i} named {filename} has been read successfully") 
                df_list.append(df)
                # Print the first 4 rows
                print(df.head(4))     
                # Replace empty strings with NaN and drop rows with missing data
                df.replace('', np.nan, inplace=True)
                columns_to_check = ['rtcTime', 'gps_Lat', 'gps_Long', 'degC', 'gps_GroundSpeed']
                rows_with_missing_data = df[df[columns_to_check].isna().any(axis=1)]
                print('\n\n Rows with missing data:')
                print(rows_with_missing_data)

# df_step1 defined --- Remove rows with missing data
                df_step1 = df.dropna(subset=columns_to_check)

            #Add a few columns to the dataframe df_step1
                df_step1 = df_step1.assign(timestamp=pd.to_datetime(df_step1['rtcDate'] + ' ' + df_step1['rtcTime']))  # Combine date and time columns into a single timestamp column
                df_step1 = df_step1.assign(Longitude=(df_step1['gps_Long'] * 1e-7))
                df_step1 = df_step1.assign(Latitude=(df_step1['gps_Lat'] * 1e-7))
                df_step1 = df_step1.assign(Altitude=(df_step1['gps_AltMSL'] * 1e-3))

                print(f"      Number of rows in raw data file: {len(df)}") 
                print(f"      Dropped {len(df) - len(df_step1)} rows with missing data")
                print(f"      Number of rows in this cleaned data file: {len(df_step1)}") 

                              
# df_step2 defined  ---  Filter out the slow speed data

                # Filter out the slow speed data
                df_step2 = df_step1[df_step1['gps_GroundSpeed'] >= cuttoff_speed]  # 447.04 mm/sec is equivalent to 1 mph  

                #df_eliminate_slow_speed.to_csv('filtered_speed.csv', index=False)
                print(f"     Total number of rows with speed above {cuttoff_speed_MPH} MPH: {len(df_step2)}_")

                

# df_step3 defined ---  Set dataframes for the time window
                print(f" \n\n timestamp_start: {timestamp_start} \n timestamp_end: {timestamp_end}_\n")

                # Convert the 'timestamp' column to datetime
                df_step2['timestamp'] = pd.to_datetime(df_step2['timestamp'])
                print(f" \n\n   Head of df_step2 after converting timestamp to datetime format  \n   {df_step2.head(10)}_")

                # Filter the data to be in the time window
                df_step3 = df_step2[(df_step2['timestamp'] > timestamp_start) & (df_step2['timestamp'] < timestamp_end)]
                print(f" \n\n    Head of df_step3 with rows in the time window:   {df_step3.head(20)}_")

                
                df_step3 = df_step3.copy()



                # Calculate 'time_delta' in seconds
                df_step3['time_delta'] = (df_step3['timestamp'] - df_step3['timestamp'].min()).dt.total_seconds()
                print(f"\n\n   Head of df_step3 with time_delta  \n  df_step3 : \n {df_step3.head(10)}_")

# df_step4 defined --- Adjust temperature drift over time
                

                df_step4 = df_step3.copy()

                df_step4['temperature_correction'] = df_step3['time_delta'] * temperature_drift
                print(f"\n\n  Head of df_step4 with added column for temperature correction: \n     {df_step4.head(10)}_")                

                df_step4['corrected_temperature'] =  df_step4['degC']  - df_step4['temperature_correction']             
               
                print(f"\n\n\n  Head of df_step4 with added column for corrected temperature:  \n  {df_step4.head(5)}_")
                print(f"\n\n    Tail of df_step4 with added column for corrected temperature: \n   {df_step4.tail(5)}_")

# df_step5 defined --- Concatenate all dataframes over the time window           
                if 'rtcTime' in df_step4 and 'degC' in df_step4:
                    df_step4['rtcTime'] = pd.to_datetime(df_step4['rtcTime'], format='%H:%M:%S.%f')
                    df_step5 = pd.concat([df_step5, df_step4], ignore_index=True)
                else:
                    print(f"File {filename} does not contain both rtcTime and degC columns", file=sys.stderr)

# df_step6 defined --- Concatenate all dataframes for the entire run including parking lot data
                df_step6 = pd.concat([df_step6, df_step1], ignore_index=True)

            except FileNotFoundError:
                print(f"File {filename} not found", file=sys.stderr)
                continue

#########################################################################################
#   End of for loop to scan all files in the directory and 
# define dataframes df_step1, df_step2, df_step3, df_step4, df_step5, df_step6
##########################################################################################

# Define the colormap for the temperature values

    if color_table_max == 0.0 or  color_table_min == 0.0:
        color_table_max = math.ceil(df_step5['corrected_temperature'].max())
        color_table_min  = math.floor(df_step5['corrected_temperature'].min())
        print(f"\n\n  color_table_max: {color_table_max}  color_table_min: {color_table_min}")
    dtemp= (color_table_max - color_table_min)/3
    index = [color_table_min, color_table_min+dtemp,color_table_min + 2 * dtemp , color_table_max] 
    print(f"\n\n  index: {index}")

    colormap = cm.LinearColormap(
        colors=['blue', 'green', 'yellow', 'red'], 
        index=index,
        vmin=color_table_min ,
        vmax=color_table_max
    )

##########################################################################################
# Overlay the coordinate pairs on the map as colored dots
##########################################################################################

# Create groups of data points for each data file

# Create a list to store groups of data points for each data file
    groups = []  # Initialize as a list
    jj = 0

    for filename in os.listdir(directory):
        if filename.endswith(".TXT"):
            # Define each group as a set of circles for each file
            group = folium.FeatureGroup(name=filename, show=True)  # show=True makes it visible initially
            for idc, row in df_step5.iterrows():
                if row['SourceFile'] == filename:
                    latitude, longitude, groundspeed = validate_and_convert(row)
                    if latitude is None or longitude is None:
                        print(f"Skipping invalid coordinate: lat={latitude}, lon={longitude}")
                        continue
                    # Determine the fill color based on temperature
                    if solid_color_by_route:
                        fill_color = solid_color_list[jj % len(solid_color_list)]                    
                    else:
                        fill_color = str(colormap(row['corrected_temperature']))

                    tooltip_text = f"File: {filename}<br>Time: {row['rtcTime']}<br>Elevation: {row['Altitude']} m <br>correctedTemp: {row['corrected_temperature']:.2f} °C <br>rawTemp: {row['degC']:.2f} °C"

                    try:
                        # Ensure temperature is valid
                        if pd.isna(row['degC']) or np.isinf(row['degC']):
                            print(f"Skipping row with invalid temperature: {row['degC']}")
                            continue

                        # Add CircleMarker for the current row
                        folium.CircleMarker(
                            location=[latitude, longitude],
                            radius=8,
                            color=fill_color,
                            fill=True,
                            fill_color=fill_color,
                            fill_opacity=0.4,
                            tooltip=tooltip_text
                        ).add_to(group)  # Add the marker to the group
                    except Exception as e:
                        print(f"Error adding marker: {latitude}, {longitude}, {fill_color}, {tooltip_text}. Error: {e}\n")

            # Add the group to the map
            group.add_to(m)
            groups.append(group)  # Store the group in the list
            jj += 1

    # Add Layer Control to toggle groups on/off
    folium.LayerControl().add_to(m)

##########################################################################################
 # Add a larger circle to indicate the location of the highest and lowest corrected temperature
##########################################################################################

    minimum_index = df_step5['corrected_temperature'].idxmin()
    Lat_min = df_step5.loc[minimum_index, 'Latitude']
    Long_min = df_step5.loc[minimum_index, 'Longitude']

    #print(f"\n\n  Minimum temperature at {Lat_min}, {Long_min}") 
    filename = df_step5.loc[minimum_index, 'SourceFile']   
    row = df_step5.loc[minimum_index] 
 
    tooltip_text = (f"File: {filename}<br>Time: {row['rtcTime']}<br>Elevation: {row['Altitude']} m <br>Min corrected Temp: {row['corrected_temperature']:.2f} °C <br>rawTemp: {row['degC']:.2f} °C ")                                                                                                                       
    folium.CircleMarker(
                                location=[ Lat_min, Long_min],
                                radius=18,
                                color='Blue',
                                fill=False,                
                                fill_color = 'Blue',
                                fill_opacity=0.0  ,
                                tooltip= tooltip_text                            
                            ).add_to(m)
    
    maximum_index = df_step5['corrected_temperature'].idxmax()
    Lat_max = df_step5.loc[maximum_index, 'Latitude']
    Long_max = df_step5.loc[maximum_index, 'Longitude']   
    print(f"\n\n  Maximum temperature at {Lat_max }, {Long_max}")
    filename = df_step5.loc[maximum_index, 'SourceFile']   
    row = df_step5.loc[maximum_index]
    tooltip_text = (f"File: {filename}<br>Time: {row['rtcTime']}<br>Elevation: {row['Altitude']} m <br>Max corrected Temp: {row['corrected_temperature']:.2f} °C <br>rawTemp: {row['degC']:.2f} °C  ")   
    folium.CircleMarker(
                                location=[Lat_max , Long_max],
                                radius=15,
                                color='Red',
                                fill=False,                
                                fill_color = 'Red',
                                fill_opacity=0.0,
                                tooltip=tooltip_text
                            ).add_to(m)               

##########################################################################################
# Add stationary sensors to the map
##########################################################################################

    # Call the sql_connection function with the start_time parameter     
    # returns list (named interpolated_temperatures) of tuples with the following columns:
    # sensorid, interpolated_temp,current_latitude, current_longitude, owners_first_name
    interpolated_temperatures = sql_connection(start_time)

    for sensor in interpolated_temperatures:   
        print(f"\n  Sensor: {sensor}")
        if sensor[1] is not None:
            tooltip_text=(f"Stationary {sensor[0]} <br>Temperature: {sensor[1]:.2f}<br>Owner: {sensor[4]}")
            fill_color = str(colormap(sensor[1]))
        else:
            tooltip_text=(f"Stationary Sensor {sensor[0]} <br>Temperature: None <br>Owner: {sensor[4]}")
            fill_color = "#000000"  # Default color or any other action
        print(f"tooltip_text: {tooltip_text}")
        folium.CircleMarker(
            location=[sensor[2], sensor[3]],
            radius=15,
            color=fill_color,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.8,
            tooltip=tooltip_text
        ).add_to(m)

##########################################################################################
# Add stationary sensors to the map
##########################################################################################
 
    colormap.caption = 'Temperature (°C)'
    colormap.add_to(m)
   
##########################################################################################
# Save the map as an HTML file
##########################################################################################
    
    if solid_color_by_route:
        filename  = './'+output_directory+'/'+color_coded_route_map
    else:
        filename  = './'+output_directory+'/'+color_coded_temperature_map
    m.save(filename)
    print(f"\n\n Map has been created and saved as {filename}\n\n")

##########################################################################################
# Plot all temperature vs. time data on one axis and save as temperaturePlot.html
##########################################################################################

    filename  = './'+output_directory+'/'+temperature_map_TimeWindow
    print(f"\n\n\  filename: {filename}")  
    fig = px.line(df_step5, x='timestamp', y='corrected_temperature', color='SourceFile', title='Time vs Corrected Temperature for the test window ')
    pio.write_html(fig, file=filename , auto_open=False)
    print(f"Combined temperature plot saved as {temperature_map_TimeWindow}")
    
    df_step6['timestamp'] = pd.to_datetime(df_step6['rtcDate'] + ' ' + df_step6['rtcTime'])
    fig = px.line(df_step6, x='timestamp', y='degC', color='SourceFile', title='Time vs Raw Temperature for entire run ')
    filename  = './'+output_directory+'/'+temperature_map_entireTime
    pio.write_html(fig, file=filename, auto_open=False)
    print(f"Combined temperature plot saved as {temperature_map_entireTime}")

##########################################################################################
# Save the final combined data in df_step5 to a CSV file
##########################################################################################

    columns_to_print = ['timestamp', 'gps_Lat', 'gps_Long', 'degC', 'gps_GroundSpeed', 'corrected_temperature', 'SourceFile']
    print(f"\n\n First 10 rows of saved data file: \n\n    df_step5.tail: \n {df_step5[columns_to_print].head(10)}_")
    print(f"\n Last 10 rows of saved data file: \n\n    df_step5.tail: \n {df_step5[columns_to_print].tail(10)}_")
    filename  = './'+output_directory+'/'+combined_data
    df_step5.to_csv(filename, index=False)   
    print(f"====================== \n    Combined data saved as {combined_data} with {len(df_step5)} rows")
# df_step7 defined
    df_step7 = df_step5[['Latitude', 'Longitude','Altitude', 'corrected_temperature','humidity_%','SourceFile']]
    filename  = './'+output_directory+'/'+combined_data_reduced_columns
    df_step7.to_csv(filename, index=False)
    print(f"====================== \n    Combined data with reduced columns saved as {combined_data_reduced_columns} with {len(df_step5)} rows")

    print(f"\n\n ================================")
    print(f"  Minimum corrected temperature: {df_step5['corrected_temperature'].min()} °C") 
    print(f"  Minimum UNcorrected temperature: {df_step5['degC'].min()} °C") 
    

    
    print(f"\n\ ================================")
    print(f"  Maximum corrected temperature: {df_step5['corrected_temperature'].max()} °C")  
    print(f"  Maximum UNcorrected temperature: {df_step5['degC'].max()} °C")
    




if __name__ == "__main__":
    # Check if a parameter was passed
    if len(sys.argv) > 1:
        # Get the command-line argument
        input_directory = sys.argv[1]
        main_process(input_directory)
    else:
        print("")
        print("  Provide input_directory as a command-line argument.")
        print("  Example: python ProcessEachRouteWithColorMap.py  InputData_Sept3")