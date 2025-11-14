import sqlite3
import functools

# -----------------------------
# Decorator 1: Handle DB connection
# -----------------------------
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


# -----------------------------
# Decorator 2: Transaction management
# -----------------------------
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Run the function inside a transaction
            result = func(conn, *args, **kwargs)
            conn.commit()        # commit if no errors
            return result
        except Exception as e:
            conn.rollback()      # rollback on error
            raise e              # re-raise the error
    return wrapper


# -----------------------------
# Function using both decorators
# -----------------------------
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


# -----------------------------
# Run example: update email
# -----------------------------
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
