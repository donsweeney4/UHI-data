import pandas as pd
import numpy as np
import folium
import sys
import os
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import branca.colormap as cm

# Assuming 'sensor_meta_data' is defined as follows:
sensor_meta_data = pd.DataFrame({
    'sensor_number': [1, 2, 3],  # Add your sensor numbers here
    'latitude': [37.6819, 37.6820, 37.6821],  # Add your latitude values here
    'longitude': [-121.7680, -121.7681, -121.7682]  # Add your longitude values here
})

# Existing code...

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

def main_process():
    directory = './OriginalData'  # Replace with your directory path
    df_list = []
    center_lat, center_lon = 37.6819, -121.7680
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)
    i = 0

    # DataFrame to hold all temperature vs. time data
    df_step5 = pd.DataFrame()
    df_step6 = pd.DataFrame()

    # Define the colormap for the temperature values
    colormap = cm.LinearColormap(
        colors=['blue', 'green', 'yellow', 'red'], 
        index=[20, 23, 26, 29],  # Assign blue to 20°C and red to 29°C
        vmin=20, 
        vmax=29
    )

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
                
                # Define df_step1, df_step2, df_step3, df_step4, df_step5, df_step6
                # (Omitted here for brevity as it's in your provided code)

                # Overlay the coordinate pairs on the map as colored dots
                for idc, row in df_step4.iterrows():
                    latitude, longitude, groundspeed = validate_and_convert(row)
                    if latitude is None or longitude is None:
                        print(f"Skipping invalid coordinate: lat={latitude}, lon={longitude}")
                        continue

                    # Determine the fill color based on temperature
                    fill_color = str(colormap(row['degC']))

                    tooltip_text = f"File: {filename}<br>Time: {row['rtcTime']}<br>Temperature: {row['degC']} °C"
                    try:
                        # Ensure temperature is valid
                        if pd.isna(row['degC']) or np.isinf(row['degC']):
                            print(f"Skipping row with invalid temperature: {row['degC']}")
                            continue
                        
                        folium.CircleMarker(
                            location=[latitude, longitude],
                            radius=8,
                            color=fill_color,
                            fill=True,                
                            fill_color=fill_color,
                            fill_opacity=0.4,
                            tooltip=tooltip_text
                        ).add_to(m)
                    except Exception as e:
                        print(f"Error adding marker: {latitude}, {longitude}, {fill_color}, {tooltip_text}. Error: {e}\n")      

                # Concatenate the dataframes
                df_step5 = pd.concat([df_step5, df_step4], ignore_index=True)
                df_step6 = pd.concat([df_step6, df_step1], ignore_index=True)

            except FileNotFoundError:
                print(f"File {filename} not found", file=sys.stderr)
                continue

    # Add stationary sensors to the map
    for _, sensor in sensor_meta_data.iterrows():
        folium.CircleMarker(
            location=[sensor['latitude'], sensor['longitude']],
            radius=12,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            tooltip=f"Sensor {sensor['sensor_number']}"
        ).add_to(m)
        
        folium.map.Marker(
            [sensor['latitude'], sensor['longitude']],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12pt; color : black">{sensor["sensor_number"]}</div>'
            )
        ).add_to(m)

    # Add the colormap legend to the map
    colormap.caption = 'Temperature (°C)'
    colormap.add_to(m)

    # Save the map as an HTML file
    m.save('map_with_coordinates.html')
    print("\n\n Map has been created and saved as map_with_coordinates.html\n\n")

    # Plot all temperature vs. time data on one axis and save as temperaturePlot.html
    fig = px.line(df_step5, x='rtcTime', y='corrected_temperature', color='SourceFile', title='Time vs Corrected Temperature for the test window ')
    pio.write_html(fig, file='temperature_WindowTime.html', auto_open=False)
    print("Combined temperature plot saved as temperature_WindowTime.html")
    
    df_step6['timestamp'] = pd.to_datetime(df_step6['rtcDate'] + ' ' + df_step6['rtcTime'])
    fig = px.line(df_step6, x='timestamp', y='degC', color='SourceFile', title='Time vs Raw Temperature for entire run ')
    pio.write_html(fig, file='temperature_EntireTime.html', auto_open=False)
    print("Combined temperature plot saved as temperature_EntireTime.html")

    # Save the final combined data to a CSV file
    columns_to_print = ['timestamp', 'gps_Lat', 'gps_Long', 'degC', 'gps_GroundSpeed', 'corrected_temperature', 'SourceFile']
    print(f"\n\n First 10 rows of saved data file: \n\n    df_step5.head: \n {df_step5[columns_to_print].head(10)}_")
    print(f"\n Last 10 rows of saved data file: \n\n    df_step5.tail: \n {df_step5[columns_to_print].tail(10)}_")

    df_step5.to_csv('combined_data.csv', index=False)   
    print(f"====================== \n    Combined data saved as combined_data.csv with {len(df_step5)} rows")

if __name__ == "__main__":
    main_process()
