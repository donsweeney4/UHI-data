# Parameters that likely change between different data sets

input_directory = 'InputData_Evening_Oct6'  # Replace with your directory path
output_directory = 'OutputData_Evening_Oct6'  # Replace with your directory path
start_time = '2024-10-06 21:20:00'
end_time = '2024-10-06 22:30:00'
cuttoff_speed_MPH = 5.0
#temperature_drift =   -0.000718 # from Alan  #-0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
temperature_drift =   -.00047# -0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
color_table_min = 20.0 #19.   # enter 0.0 to use floor of minimum temperature in data
color_table_max = 30.0 #29.   # enter 0.0 to use ceiling of maximum temperature in data

# Parameters that likely don't change between different data sets

solid_color_by_route = False # if true, color by route, if false, color by temperature
color_coded_temperature_map = 'color_coded_temperature_map.html'
color_coded_route_map = 'color_coded_route_map.html'
temperature_map_TimeWindow = 'temperaturePlot_TimeWindow.html'
temperature_map_entireTime = 'temperature_EntireTime.html'
combined_data = 'combined_data.csv'
combined_data_reduced_columns = 'combined_data_reduced_columns.csv'