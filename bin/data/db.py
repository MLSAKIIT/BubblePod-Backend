from configparser import ConfigParser
import psycopg2
from typing import Dict


def load_connection_info(ini_filename: str) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "accounts" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("accounts")}
    return conn_info


def create_db(conn_info: Dict[str, str],) -> None:
    # Connect just to PostgreSQL with the user loaded from the .ini file
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False


def create_table(sql_query: str, conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()





# host, database, user, password
conn_info = load_connection_info("db.ini")

# Create the desired database
create_db(conn_info)

# Connect to the database created
connection = psycopg2.connect(**conn_info)
cursor = connection.cursor()

# Create the "house" table
query = """
    CREATE TABLE IF NOT EXISTS accounts (
    user_id serial PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP NOT NULL,
    interest1 VARCHAR(50) NOT NULL,
    interest2 VARCHAR(50) NOT NULL,
    interest3 VARCHAR(50) NOT NULL,
    cluster INT UNIQUE NOT NULL);
"""
create_table(query, connection, cursor)

# Close all connections to the database
connection.close()
cursor.close()