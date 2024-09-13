 
 # Parameters that likely change between different data sets

input_directory = 'InputData_Sept3_trials'  # Replace with your directory path
output_directory = 'OutputData_Sept3_trials'  # Replace with your directory path
start_time = '2024-09-03 21:26:00'
end_time = '2024-09-03 22:45:00'
cuttoff_speed_MPH = 5.0
#temperature_drift =   -0.000718 # from Alan  #-0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
temperature_drift =   -0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
color_table_min = 0.0 #19.   # enter 0.0 to use floor of minimum temperature in data
color_table_max = 0.0 #29.   # enter 0.0 to use ceiling of maximum temperature in data

# Parameters that likely don't change between different data sets

solid_color_by_route = False # if true, color by route, if false, color by temperature
color_coded_temperature_map = 'color_coded_temperature_map.html'   # Output .html file with temperature map - output if solid_color_by_route = False
color_coded_route_map = 'color_coded_route_map.html'  # Output .html file with route map - output if solid_color_by_route = True
temperature_map_TimeWindow = 'temperaturePlot_TimeWindow.html'
temperature_map_entireTime = 'temperature_EntireTime.html'
combined_data = 'combined_data.csv'   # Output .csv file with all processed data and all columns 
combined_data_reduced_columns = 'combined_data_reduced_columns.csv'  # Output .csv file with fewer columns for easier viewing and debugging