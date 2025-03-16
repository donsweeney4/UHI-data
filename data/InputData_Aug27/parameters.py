# Define the time window for the data
input_directory = 'InputData_Aug27'  # Replace with your directory path
output_directory = 'OutputData_Aug27'  # Replace with your directory path
start_time =  '2024-08-27 20:45:00'
end_time =    '2024-08-27 22:00:45'
cuttoff_speed_MPH = 5.0
temperature_drift = -0.000487  #  Adjust temperature drift over time     - based on Sensor10 @ 3m 

color_table_min = 0.0 #19.   # enter 0.0 to use floor of minimum temperature in data
color_table_max = 0.0 #29.   # enter 0.0 to use ceiling of maximum temperature in data

# Parameters that likely don't change between different data sets

solid_color_by_route = True # if true, color by route, if false, color by temperature
color_coded_temperature_map = 'color_coded_temperature_map.html'
color_coded_route_map = 'color_coded_route_map.html'
temperature_map_TimeWindow = 'temperaturePlot_TimeWindow.html'
temperature_map_entireTime = 'temperature_EntireTime.html'
combined_data = 'combined_data.csv'
combined_data_reduced_columns = 'combined_data_reduced_columns.csv'

