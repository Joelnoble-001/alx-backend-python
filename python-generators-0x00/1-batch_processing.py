#!/usr/bin/python3
from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches using yield"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch      # YIELD keyword (not return)
            batch = []

    if batch:
        yield batch          # YIELD remaining records

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
