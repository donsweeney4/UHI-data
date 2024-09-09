import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load the temperature data
data = pd.read_csv('./OutputData_Sept3_trials/combined_data_reduced_columns.csv')

# Extract latitude, longitude, and temperature
latitudes = data['Latitude'].values
longitudes = data['Longitude'].values
temperatures = data['corrected_temperature'].values

# Print min/max of actual temperatures to confirm they are correct
print(f"min temperatures: {min(temperatures)}")
print(f"max temperatures: {max(temperatures)}")

# Create grid for interpolation (ensure grid covers full data range)
maxlong=-121.69
grid_lat, grid_lon = np.mgrid[min(latitudes):max(latitudes):100j, min(longitudes):maxlong:100j]


# Interpolate temperature values over the grid
grid_temperature = griddata((latitudes, longitudes), temperatures, (grid_lat, grid_lon), method='linear')

# Debugging step: Print the min/max of the interpolated temperature grid
#print(f"min grid temperatures: {np.nanmin(grid_temperature)}")
#print(f"max grid temperatures: {np.nanmax(grid_temperature)}")

# Plot the contour map with manually set color scale limits
plt.figure(figsize=(8, 6))
contour = plt.contourf(grid_lon, grid_lat, grid_temperature, cmap='coolwarm', vmin=min(temperatures), vmax=max(temperatures))  # Manually set vmin and vmax to actual temperature range
plt.colorbar(label='Temperature (°C)')

# Scatter plot of original data points
plt.scatter(longitudes, latitudes, c=temperatures, edgecolor='black', cmap='coolwarm', marker='o', s=20)
plt.title('Temperature Contour Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Set plot limits to match grid
plt.xlim(min(longitudes), maxlong)
plt.ylim(min(latitudes), max(latitudes))

plt.show()
