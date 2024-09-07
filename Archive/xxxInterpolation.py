import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
import plotly.graph_objects as go
from quart import Quart, render_template_string

# Initialize the Quart app
app = Quart(__name__)

# Load your data from a CSV file (replace 'your_data.csv' with your actual file)
# The CSV file should have columns: 'longitude', 'latitude', 'temperature'
data = pd.read_csv('./filtered_speed.csv')

# Extract the coordinates and temperature values
lons = data['gps_Long'].values * 1.e-7
lats = data['gps_Lat'].values * 1.e-7   
temps = data['degC'].values

# Define the grid over the area you want to interpolate
grid_lon = np.linspace(-121.8207452, -121.7694379, 10)
grid_lat = np.linspace(37.6811748, 37.7120178, 10)
grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

# Perform Ordinary Kriging
print("Performing Ordinary Kriging...") 
OK = OrdinaryKriging(lons, lats, temps, variogram_model='linear', verbose=False, enable_plotting=False)
z, ss = OK.execute('grid', grid_lon, grid_lat)

# Create a Plotly figure for the contour map
fig = go.Figure(data=[
    go.Contour(
        z=z,
        x=grid_lon[0],  # x-axis is longitude
        y=grid_lat[:, 0],  # y-axis is latitude
        colorscale='Jet',
        contours=dict(start=z.min(), end=z.max(), size=(z.max() - z.min()) / 10),
        colorbar=dict(title='Temperature (°C)')
    ),
    go.Scatter(
        x=lons,
        y=lats,
        mode='markers',
        marker=dict(color=temps, colorscale='Jet', size=8, line=dict(width=1, color='black')),
        name='Data Points'
    )
])

# Customize the layout
fig.update_layout(
    title='Temperature Contour Map - Livermore, CA',
    xaxis_title='Longitude',
    yaxis_title='Latitude',
    height=600
)

# Define the HTML template with Plotly
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Temperature Contour Map</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="plot"></div>
    <script>
        var plot_data = {{ plot_data | safe }};
        Plotly.newPlot('plot', plot_data.data, plot_data.layout);
    </script>
</body>
</html>
"""


# Quart route to serve the map
@app.route('/')
async def index():
    plot_data = fig.to_plotly_json()
    return await render_template_string(template, plot_data=plot_data)

# Run the Quart app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
