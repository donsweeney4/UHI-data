# Define the time window for the data
input_directory = 'InputData_Sept3'  # Replace with your directory path
output_directory = 'OutputData_Sept3_trials'  # Replace with your directory path
start_time = '2024-09-03 21:26:00'
end_time = '2024-09-03 22:45:00'
cuttoff_speed_MPH = 5.0
#temperature_drift =   -0.000718 # from Alan  #-0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
temperature_drift =   -0.000487  #  Adjust temperature drift over time- based on Sensor10 @ 3m 
color_coded_temperature_map = 'color_coded_temperature_map.html'
temperature_map_TimeWindow = 'temperaturePlot_TimeWindow.html'
temperature_map_entireTime = 'temperature_EntireTime.html'
color_table_min = 19.
color_table_max = 29.
combined_data = 'combined_data.csv'
combined_data_reduced_columns = 'combined_data_reduced_columns.csv'

stationary_sensor_meta_data = {
    'sensor_number': [ '1','10','11','12','2','21','22','23','24','25','26','27','3','4','5','51','52','6','7','8','9'],
    'latitude': [37.654,37.6599,37.6489,37.6489,37.7439,37.6737,37.7345,37.6894,37.6841,37.68,37.6728,37.6867,37.6869,37.7258,37.7033,37.6829,37.693851,37.6825,37.6762,37.7142,37.665],
    'longitude': [-121.775,-121.805,-121.762,-121.762,-121.425,-121.755,-121.47,-121.778,-121.731,-121.743,-121.796,-121.785,-121.884,-121.712,-121.793,-121.77,-121.715688,-121.77,-121.74,-121.721,-121.763],
    'temperature': [0.,25.6,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,20.3,27.25,23.67,0.,26.26]                
}
