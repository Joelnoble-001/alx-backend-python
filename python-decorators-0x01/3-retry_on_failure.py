import time
import sqlite3
import functools

# ---------------------------------
# Decorator: Handle DB connection
# ---------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


# ---------------------------------
# Decorator: Retry on failure
# ---------------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")

                    if attempts == retries:
                        print("All retries failed.")
                        raise e     # re-raise final error

                    time.sleep(delay)  # wait before retrying

        return wrapper
    return decorator


# ---------------------------------
# Using both decorators
# ---------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# ---------------------------------
# Run the function
# ---------------------------------
users = fetch_users_with_retry()
print(users)
