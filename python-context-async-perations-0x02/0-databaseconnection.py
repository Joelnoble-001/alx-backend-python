import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection
        if self.conn:
            self.conn.close()
        # Returning False means errors (if any) are not suppressed
        return False


# -----------------------------------------
# Using the custom context manager
# -----------------------------------------

with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    print(results)
