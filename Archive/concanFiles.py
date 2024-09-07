import os
import pandas as pd

# Directory containing the TXT files
directory = './'  # Replace with your directory path

# List to store dataframes
df_list = []

# Loop through all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".TXT"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        df_list.append(df)

# Concatenate all dataframes, ignoring the header row except for the first file
combined_df = pd.concat(df_list, ignore_index=True)

# Assuming your dataframe is named df and has 'longitude' and 'latitude' columns
min_longitude = df['gps_Long'].min()
max_longitude = df['gps_Long'].max()

min_latitude = df['gps_Lat'].min()
max_latitude = df['gps_Lat'].max()

print(f"Minimum Longitude: {min_longitude}")
print(f"Maximum Longitude: {max_longitude}")
print(f"Minimum Latitude: {min_latitude}")
print(f"Maximum Latitude: {max_latitude}")

# Save the combined dataframe to a CSV file
#output_file_path = os.path.join(directory, 'summary_file.csv')
#combined_df.to_csv(output_file_path, index=False)

