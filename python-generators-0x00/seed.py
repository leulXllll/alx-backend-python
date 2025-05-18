import mysql.connector
from mysql.connector import errorcode
import uuid
import csv

# Connect to the MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the ALX_prodev database if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

# Connect directly to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Insert data from CSV file into the table if it doesn't already exist
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check for duplicates using email
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
                if not cursor.fetchone():
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        str(uuid.uuid4()),
                        row['name'],
                        row['email'],
                        row['age']
                    ))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
