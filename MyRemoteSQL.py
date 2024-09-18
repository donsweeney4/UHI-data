import mysql.connector
from mysql.connector import Error

def sql_connection(start_time):
    connection = None  # Initialize the connection variable
    interpolated_temperatures_list = []  # Initialize list to store temperatures

    try:
        # Define the connection parameters
        connection = mysql.connector.connect(
            host='100.20.98.153',  # e.g., 'example.com'
            port=3306,  # default MySQL port
            database='uhi',
            user='uhi',
            password='uhi'
        )
        if connection.is_connected():
            print("Connected to the database")

            # Create a cursor object
            cursor = connection.cursor()

            # Fetch distinct sensor IDs
            cursor.execute("SELECT DISTINCT(sensorid) FROM sensor_data;")
            distinct_sensor_ids = cursor.fetchall()  # Fetch all distinct sensor ids

            # Loop through each sensorid and call the stored procedure
            for sensorid_tuple in distinct_sensor_ids:
                sensorid = sensorid_tuple[0]  # Extract sensorid from tuple
                print(f"Get interpolated temp for Sensor ID: {sensorid}")

                # Execute the stored procedure
                cursor.callproc('interpolated_temperature_for_sensor', [start_time, sensorid])

                # Fetch the result of the SELECT statement within the procedure
                for result in cursor.stored_results():
                    rows = result.fetchall()

                    # Iterate over each row and process
                    for row in rows:
                        # Check if row has enough elements before accessing them
                        if len(row) >= 5:
                            print(f"Row: {row}")
                            # Append sensorid and temperature to list (sensorid, interpolated_temp)
                            interpolated_temperatures_list.append((sensorid, row[1],row[2],row[3],row[4]))  # Assuming row[1] is interpolated_temp
                        else:
                            # Handle case where debug messages or incomplete data is returned
                            print(f"Unexpected row format: {row}")

            return interpolated_temperatures_list
        

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        # Ensure connection is closed if it was opened
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


######################################################################################
# Test the sql_connection function
######################################################################################

def test_sql_connection():
    # Define a sample start_time for testing
    test_start_time = '2024-09-03 21:00:00'  # Replace with an appropriate timestamp
    
    # Call the sql_connection function
    interpolated_temperatures = sql_connection(test_start_time)
    
    # Check if the interpolated temperatures are returned correctly
    if interpolated_temperatures:
        print("Test Passed!")
        print("\nInterpolated Temperature Results:")
        for sensorid, temperature,latitude,longitude,owners_name in interpolated_temperatures:
            print(f"Sensor ID: {sensorid}, Interpolated Temperature: {temperature}, Latitude: {latitude}, Longitude: {longitude}, Owner's Name: {owners_name}")
            #print(f"Sensor ID: {sensorid}, Interpolated Temperature: {temperature}")
    else:
        print("Test Failed! No data returned or an error occurred.")

# Ensure the test function only runs when the script is executed directly
if __name__ == "__main__":
    test_sql_connection()
