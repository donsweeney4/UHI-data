import mysql.connector
from mysql.connector import Error

def sql_connection():
    try:
        # Define the connection parameters
        connection = mysql.connector.connect(
            host='
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
        
 # Execute the SHOW TABLES command to list all tables in the database
        cursor.execute("SHOW TABLES;")
        
        # Fetch and display the list of tables
        tables = cursor.fetchall()

        print("Tables in the database:")
        for table in tables:
            print(table)

        # You can also execute other queries, such as selecting data
        cursor.execute("SELECT * FROM latest_sensor_meta_data ;")
        results = cursor.fetchall()
        
        print("\nSample data from your_table_name:")
        for row in results:
            print(row)

        return tables, results

        
except Error as e:
    return None, None
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
 
