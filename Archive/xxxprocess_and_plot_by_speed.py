import pandas as pd
import numpy as np
import folium
import argparse
import sys
import plotly.express as px
import plotly.io as pio
from datetime import datetime

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

def main(input_file):
    # Read the CSV file and print the first 10 rows
    try:
        df = pd.read_csv(input_file)
        for i in range(10):
            print(df.iloc[i])   # Print the first 10 rows
    
    except FileNotFoundError:
        print(f"File {input_file} not found", file=sys.stderr)
        sys.exit(1)

 

    # Print the columns of the DataFrame to debug the column names
    print("\n\n Columns in the CSV file:", df.columns)
#############################################################################################################
    # Move through the dataframe and find rows that are more than {sampleinterval} apart
    #   Convert the 'gps_Time' column to a datetime object


############################################################################################################
    # Preprocess the data rows to drop rows with blank, NULL, or NaN values, print those rows
    # Replace empty strings with NaN
    df.replace('', np.nan, inplace=True)
    # Specify the columns to check
    columns_to_check = ['rtcTime','gps_Lat', 'gps_Long','degC', 'gps_GroundSpeed']
    # Find rows where any of the specified columns have NaN and print them
    rows_with_missing_data = df[df[columns_to_check].isna().any(axis=1)]
    print('\n\n Rows with missing data:')
    print(rows_with_missing_data)
    # Drop rows with NaN in the specified columns
    df_cleaned = df.dropna(subset=columns_to_check)

    print(f"\n Number of rows in raw data file: {len(df)}") 
    print(f"\n Dropped {len(df) - len(df_cleaned)} rows with missing data")
    print(f"\n Number of rows in cleaned data file: {len(df_cleaned)}")                   
  


#############################################################################################################
    # Center of Livermore, California
    center_lat, center_lon = 37.6819, -121.7680

    # Create a map centered around Livermore, California with initial zoom level of 18
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Overlay the coordinate pairs on the map as small colored dots
    
    ncount_red = 0;
    ncount_orange = 0;
    ncount_purple = 0;    
    ncount_yellow = 0;
    ncount_green = 0;
    ncount_blue = 0;

    row_total = 0

    for  idc,row in df_cleaned.iterrows():
        
        
        latitude, longitude, groundspeed = validate_and_convert(row)
        row_total = row_total + 1
        print(f"Row {idc} has groundspeed: {groundspeed}")    
                
        if groundspeed < 10.0:
            fill_color = 'red'
            ncount_red = ncount_red + 1
        elif groundspeed < 15.0:
            fill_color = 'orange'
            ncount_orange = ncount_orange + 1
 
        elif groundspeed < 20.0:
            fill_color= 'purple'
            ncount_purple = ncount_purple + 1 

        elif groundspeed < 25.0:
            fill_color = 'yellow'
            ncount_yellow = ncount_yellow + 1
  
                  
        elif groundspeed > 35.0:
            fill_color = 'blue'
            ncount_blue = ncount_blue + 1 
        else:
            fill_color = 'green'
            ncount_green = ncount_green + 1
                    #print(f"green point with speed: {groundspeed}")
                  


        folium.CircleMarker(
            location=[latitude, longitude],
            radius=2,
            color=fill_color,
            fill=True,                fill_color=fill_color,
            ).add_to(m) 

    # Save the map as an HTML file
    m.save('map_with_coordinates.html')
    print("\n\n Map has been created and saved as map_with_coordinates.html\n\n")

    print("Number at  0-10 MPH (red):   ", ncount_red) # Print the number of points plotted
    print("Number at 10-15MPH (orange): ", ncount_orange) # Print the number of points plotted
    print("Number at 15-20MPH (purple): ", ncount_purple) # Print the number of points plotted   
    print("Number at 20-25MPH (yellow): ", ncount_yellow) # Print the number of points plotted
    print("Number at 25-35MPH (green):  ", ncount_green) # Print the number of points plotted
    print("Number at   >35MPH (blue):   ", ncount_blue) # Print the number of points plotted

    print("\n\n Row total from above: ", row_total)

    # Plot rtcTime vs degC using Plotly
    if 'rtcTime' in df.columns and 'M3 degC' in df.columns:
        fig = px.line(df, x='rtcTime', y='M3 degC', title='Temperature Over Time')
        pio.write_html(fig, file='temperature_plot.html', auto_open=True)
        print("\n\n\ Plot has been created and saved as temperature_plot.html")
    else:
        print("\n CSV file does not contain both rtcTime and M3 degC  columns", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a CSV file and plot points on a map.')
    parser.add_argument('--input', required=True, help='Input CSV file name')
    args = parser.parse_args()

    main(args.input)
