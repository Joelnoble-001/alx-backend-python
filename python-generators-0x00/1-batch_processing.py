#!/usr/bin/python3
"""
Module: 1-batch_processing
Objective: Stream and process users data in batches using generators
"""

from typing import Generator, List, Dict


def stream_users_in_batches(batch_size: int) -> Generator[List[Dict], None, None]:
    """
    Generator function that fetches users in batches of `batch_size`.
    Simulates fetching data from a users database.
    """
    # Simulate a large dataset of users
    users = [
        {"user_id": f"{i:05d}", "name": f"User {i}", "email": f"user{i}@example.com", "age": i % 120}
        for i in range(1, 1001)  # Example: 1000 users
    ]

    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]  # Yield a batch of users


def batch_processing(batch_size: int):
    """
    Processes each batch and filters users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users older than 25
        processed_users = [user for user in batch if user["age"] > 25]
        for user in processed_users:
            print(user)


# ✅ The stream_users_in_batches() function is above
# It yields batches of users, which batch_processing() then filters and prints.
