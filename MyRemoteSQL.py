import mysql.connector
from mysql.connector import Error

def sql_connection(start_time):
    connection = None  # Initialize the connection variable
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

            # Interpolate temperature using the start_time parameter
            cursor.execute(f"CALL interpolated_temperatures('{start_time}');")  # Stored procedure returns result directly
            interpolated_temperatures = cursor.fetchall()  # Fetch the result set from the procedure call

            return interpolated_temperatures

    except Error as e:
        print(f"Error: {e}")
        return None, None

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
    test_start_time = '2024-08-05 12:00:00'  # Replace with an appropriate timestamp
    
    # Call the sql_connection function
    results, interpolated_temperature = sql_connection(test_start_time)
    
    # Check if the results and interpolated temperatures are returned correctly
    if results is not None and interpolated_temperature is not None:
        print("Test Passed!")
        print("Results from latest_sensor_meta_data:")
        for row in results:
            print(row)
        
        print("\nInterpolated Temperature Results:")
        for row in interpolated_temperature:
            print(row)
    else:
        print("Test Failed! No data returned or an error occurred.")

# Ensure the test function only runs when the script is executed directly
if __name__ == "__main__":
    test_sql_connection()
