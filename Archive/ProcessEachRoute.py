import pandas as pd
import numpy as np
import folium
import sys
import os

def validate_and_convert(row):
    try:
        # Validate and convert latitude, longitude
        latitude = float(row['gps_Lat']) * 1e-7
        longitude = float(row['gps_Long']) * 1e-7
        groundspeed = float(row['gps_GroundSpeed']) * 0.00223694  # Convert m/s to mph
        return latitude, longitude, groundspeed
    except ValueError as e:
        print(f"Error processing row {row}: {e}", file=sys.stderr)
        return None, None, None

def main_process():
    directory = './OriginalData_Aug27'  # Replace with your directory path
    df_list = []
    fill_color_list = ['red', 'yellow', 'green', 'blue'] 
    center_lat, center_lon = 37.6819, -121.7680
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    i = 0
    row_total = 0  # Initialize row_total

    for filename in os.listdir(directory):
        if filename.endswith(".TXT"):
            fill_color = fill_color_list[i % len(fill_color_list)] 
            i += 1  # Increment the index to change the fill color
            file_path = os.path.join(directory, filename)

            # Read the CSV file
            try:
                df = pd.read_csv(file_path)
                df_list.append(df)

                # Print the first 10 rows
                print(df.head(10))   

                # Print the columns of the DataFrame to debug the column names
                print("\n\n Columns in the CSV file:", df.columns)

                # Replace empty strings with NaN and drop rows with missing data
                df.replace('', np.nan, inplace=True)
                columns_to_check = ['rtcTime', 'gps_Lat', 'gps_Long', 'degC', 'gps_GroundSpeed']
                rows_with_missing_data = df[df[columns_to_check].isna().any(axis=1)]
                print('\n\n Rows with missing data:')
                print(rows_with_missing_data)
                df_cleaned = df.dropna(subset=columns_to_check)

                print(f"\n\n    File {i} named {filename} has been read successfully")   
                print(f"      Number of rows in raw data file: {len(df)}") 
                print(f"      Dropped {len(df) - len(df_cleaned)} rows with missing data")
                print(f"      Number of rows in this cleaned data file: {len(df_cleaned)}")                   

                # Overlay the coordinate pairs on the map as small colored dots
                for idc, row in df_cleaned.iterrows():
                    latitude, longitude, groundspeed = validate_and_convert(row)
                    if latitude is None or longitude is None:
                        continue
                    row_total += 1
                    #print(f"Row {idc} has groundspeed: {groundspeed}")

                    folium.CircleMarker(
                        location=[latitude, longitude],
                        radius=2,
                        color=fill_color,
                        fill=True,                
                        fill_color=fill_color,
                    ).add_to(m) 

            except FileNotFoundError:
                print(f"File {filename} not found", file=sys.stderr)
                continue
        # filter on timestamp
            #df_cleaned['rtcTime'] = pd.to_datetime(df_cleaned['rtcTime'], unit='s')

        # filter out the slow speed datadf_eliminate_slow_speed = df_cleaned[df_cleaned['gps_GroundSpeed'] > 4470.4]
            df_eliminate_slow_speed = df_cleaned[df_cleaned['gps_GroundSpeed'] >= 4470.4]        # 4470.4 mm/sec is equivalent to 10 mph   
            df_eliminate_slow_speed.to_csv('filtered_speed.csv', index=False)

            row_total = len(df_cleaned) 
            row_total10 = len(df_eliminate_slow_speed)  
            print(f"\n\n Total number of rows of all data : {row_total}")   
            print(f"\n\n Total number of rows with speed above 10 MPH: {row_total10}_")

                   
    # Save the map as an HTML file
    m.save('map_with_coordinates.html')
    print("\n\n Map has been created and saved as map_with_coordinates.html\n\n")

if __name__ == "__main__":
    main_process()
