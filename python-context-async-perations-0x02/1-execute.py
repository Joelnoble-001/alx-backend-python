import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        # Execute the query when entering
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)

        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
        # Returning False allows exceptions to propagate
        return False

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
