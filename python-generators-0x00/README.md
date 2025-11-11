# 0x00. Python - Generators

## Tasks

### 0. Getting started with python generators

Write a Python script `seed.py` that:

- Connects to a MySQL server.
- Creates a database `ALX_prodev` if it does not exist.
- Connects to the `ALX_prodev` database.
- Creates a table `user_data` with the following fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table using data from `user_data.csv`.

**Prototypes:**
```python
def connect_db()
def create_database(connection)
def connect_to_prodev()
def create_table(connection)
def insert_data(connection, data)
