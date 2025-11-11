#!/usr/bin/python3
"""
Generator that streams rows from the user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator function that yields rows from user_data table one by one."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔒 Replace with your MySQL password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")
        if connection.is_connected():
            cursor.close()
            connection.close()
