import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import pytz  # For timezone handling

def fit_temperature(csv_input_file, start_time, end_time, timezone='UTC'):
    # Read the CSV file
    df = pd.read_csv(csv_input_file)

    # Define the timezone
    tz = pytz.timezone(timezone)

    # Combine 'rtcDate' and 'rtcTime' into a single datetime column
    df['datetime'] = pd.to_datetime(df['rtcDate'] + ' ' + df['rtcTime'])

    # If the 'datetime' column is already tz-aware, use tz_convert; otherwise, use tz_localize
    if pd.api.types.is_datetime64tz_dtype(df['datetime']):
        df['datetime'] = df['datetime'].dt.tz_convert(tz)
    else:
        df['datetime'] = df['datetime'].dt.tz_localize(tz)

    # Convert the start_time and end_time input strings to timezone-aware datetime objects
    start_time_dt = pd.to_datetime(start_time, format='%m/%d/%Y %H:%M:%S').tz_localize(tz)
    end_time_dt = pd.to_datetime(end_time, format='%m/%d/%Y %H:%M:%S').tz_localize(tz)

    # Filter the dataframe to include only rows between start_time and end_time
    df_filtered = df[(df['datetime'] >= start_time_dt) & (df['datetime'] <= end_time_dt)]

    if df_filtered.empty:
        print("No data available within the specified time range.")
        return

    # Calculate time in seconds from the first timestamp in the filtered data
    df_filtered['time_seconds'] = (df_filtered['datetime'] - df_filtered['datetime'].min()).dt.total_seconds()

    # Extract temperature and time columns for regression
    X = df_filtered[['time_seconds']].values  # Time in seconds
    y = df_filtered['degC'].values  # Temperature in degrees Celsius

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Get the slope of the line (degrees per second)
    slope = model.coef_[0]

    # Print the slope
    print(f"Slope of the linear fit: {slope} degrees per second")

# Example usage
csv_input_file = '.\OutputData_Afternoon_Oct6\combined_data.csv'  # replace with the actual file path
start_time = '10/06/2024 16:32:00'  # Example start time
end_time = '10/06/2024 17:52:00'  # Example end time

fit_temperature(csv_input_file, start_time, end_time)
