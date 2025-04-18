import sys
import pandas as pd
from datetime import datetime
import pytz

# Mapping of old to new column names
COLUMN_MAP = {
    'rtcDate': 'Local Date',
    'rtcTime': 'Local Time',
    'gps_Lat': 'Latitude',
    'gps_Long': 'Longitude',
    'gps_AltMSL': 'Altitude (m)',
    'gps_GroundSpeed': 'Speed (MPH)',
    'humidity_%': 'Humidity (%)',
    'degC': 'Temperature (°C)'
}


def transform_csv(input_file, output_file, jobcode):
    # Read CSV
    df = pd.read_csv(input_file)

    # Drop unknown columns (those not in COLUMN_MAP or expected new columns)
    expected_old = set(COLUMN_MAP.keys())
    known_columns = set(COLUMN_MAP.values()).union({'rownumber', 'jobcode', 'Timestamp', 'Accuracy (m)'})
    df = df[[col for col in df.columns if col in expected_old]]

    # Rename columns
    df = df.rename(columns=COLUMN_MAP)

    # Add rownumber
    df.insert(0, 'rownumber', range(1, len(df) + 1))

    # Add jobcode
    df.insert(1, 'jobcode', jobcode)

    # Add Timestamp column from Local Date and Local Time in US/Pacific, convert to UTC and represent as integer timestamp
    local_tz = pytz.timezone('US/Pacific')
    df['Timestamp'] = pd.to_datetime(df['Local Date'] + ' ' + df['Local Time'], errors='coerce')
    df['Timestamp'] = df['Timestamp'].dt.tz_localize(local_tz, ambiguous='NaT', nonexistent='NaT').dt.tz_convert('UTC')
    df['Timestamp'] = df['Timestamp'].astype('int64') // 10**9  # Convert to seconds since epoch

    # Add Accuracy (m) column with value 0
    df['Accuracy (m)'] = 0

    # Convert speed from mm/s to MPH (1 mm/s = 0.00223694 MPH), truncate to 2 decimal places
    if 'Speed (MPH)' in df.columns:
        df['Speed (MPH)'] = (pd.to_numeric(df['Speed (MPH)'], errors='coerce') * 0.00223694).round(2)

    # Scale Latitude and Longitude by 1e-7, truncate to 5 decimal places
    for col in ['Latitude', 'Longitude']:
        if col in df.columns:
            df[col] = (pd.to_numeric(df[col], errors='coerce') * 1e-7).round(5)

    # Scale Altitude (m) by 1e-3 and truncate to 1 decimal place
    if 'Altitude (m)' in df.columns:
        df['Altitude (m)'] = (pd.to_numeric(df['Altitude (m)'], errors='coerce') * 1e-3).round(1)

    # Truncate Temperature (°C) to 2 decimal places
    if 'Temperature (°C)' in df.columns:
        df['Temperature (°C)'] = pd.to_numeric(df['Temperature (°C)'], errors='coerce').round(2)

    # Save to output CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Output written to {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python transform_csv.py input.csv output.csv jobcode")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    jobcode = sys.argv[3]
    transform_csv(input_csv, output_csv, jobcode)
