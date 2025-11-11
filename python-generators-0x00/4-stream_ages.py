#!/usr/bin/python3
"""
Module: 4-stream_ages
Objective: Compute the average age of users efficiently using a generator.
"""

import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔒 replace with your MySQL password
            database="ALX_prodev"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")

        for (age,) in cursor:
            yield age

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error while streaming user ages: {e}")
        try:
            if connection.is_connected():
                cursor.close()
                connection.close()
        except:
            pass


def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate and print the average age
    without loading all data into memory.
    """
    total_age = 0
    count = 0

    # 🔹 First loop: iterate over generator to accumulate total and count
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()
