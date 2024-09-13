"""
Python script to interpolate temperature data using Kriging and plot a contour map.



"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pykrige.ok import OrdinaryKriging


def main_process(input_file):
    # Load the temperature data
    data = pd.read_csv(input_file)

    # Extract latitude, longitude, and temperature
    latitudes = data['Latitude'].values
    longitudes = data['Longitude'].values
    temperatures = data['corrected_temperature'].values

    # Print min/max of actual temperatures to confirm they are correct
    print(f"min temperatures: {min(temperatures)}")
    print(f"max temperatures: {max(temperatures)}")

    # Define the grid for interpolation (same as linear interpolation)
    maxlong = -121.74  # Define fixed max longitude if needed
    grid_lat, grid_lon = np.mgrid[min(latitudes):max(latitudes):100j, min(longitudes):maxlong:100j]

    # Create Kriging model (longitude first, then latitude)
    kriging_model = OrdinaryKriging(longitudes, latitudes, temperatures, variogram_model='linear')

    # Interpolate over a grid (Note the consistent use of grid_lon and grid_lat)
    grid_temperature, ss = kriging_model.execute('grid', grid_lon[0,:], grid_lat[:,0])

    # Print the min/max of the interpolated temperature grid (debugging step)
    print(f"min grid temperatures: {np.nanmin(grid_temperature)}")
    print(f"max grid temperatures: {np.nanmax(grid_temperature)}")

    # Define a custom colormap from blue to cyan to green to yellow to red
    colors = ['blue', 'cyan', 'green', 'yellow', 'red']
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)

    # Plot the contour map with manually set color scale limits
    plt.figure(figsize=(8, 6))
    contour = plt.contourf(grid_lon, grid_lat, grid_temperature, cmap=custom_cmap, vmin=35.35, vmax=37.5)
    plt.colorbar(label='Temperature (°C)')

    # Scatter plot of original data points
    plt.scatter(longitudes, latitudes, c=temperatures, edgecolor='black', cmap=custom_cmap, marker='o', s=50)
    plt.title('Temperature Contour Map (Kriging Interpolation)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Set plot limits to match grid
    plt.xlim(min(longitudes), maxlong)
    plt.ylim(min(latitudes), max(latitudes))

    plt.show()


if __name__ == "__main__":
    # Check if a parameter was passed
    if len(sys.argv) > 1:
        # Get the command-line argument
        input_file = sys.argv[1]
        main_process(input_file)
    else:
        print("")
        print("   Provide input_file as a command-line argument.")
        print("   Example: python interpolation4.py ./outputData_Sept3/combined_data_reduced_columns.csv")
