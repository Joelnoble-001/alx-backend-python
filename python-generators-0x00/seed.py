#!/usr/bin/python3
"""
Seed script for creating and populating the ALX_prodev MySQL database.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connect to MySQL server (without specifying database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # 🔒 replace with your actual MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔒 replace with your actual MySQL password
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10, 0) NOT NULL,
            INDEX idx_user_id (user_id)
        );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from user_data.csv into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("name")
                email = row.get("email")
                age = row.get("age")

                # Avoid duplicate emails
                cursor.execute("SELECT email FROM user_data WHERE email = %s;", (email,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                        (str(uuid.uuid4()), name, email, age)
                    )

        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except FileNotFoundError:
        print(f"Error: file '{csv_file}' not found.")
    except Error as e:
        print(f"Error inserting data: {e}")
