import time
import sqlite3 
import functools

query_cache = {}

# ---------------------------------
# Decorator: Handle DB connection
# (paste from previous task)
# ---------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# ---------------------------------
# Decorator: Cache Query Results
# ---------------------------------
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract SQL query (positional or keyword)
        query = None

        if args:
            # First argument after conn is the query
            query = args[0]
        elif "query" in kwargs:
            query = kwargs["query"]

        # Check if result is in cache
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]

        # Cache miss → run query normally
        print(f"Cache miss. Running query: {query}")
        result = func(conn, *args, **kwargs)

        # Store in cache
        query_cache[query] = result
        return result

    return wrapper


# ---------------------------------
# Function using the decorators
# ---------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ---------------------------------
# Test the cache
# ---------------------------------
print("First call (should run query):")
users = fetch_users_with_cache(query="SELECT * FROM users")

print("\nSecond call (should use cache):")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
