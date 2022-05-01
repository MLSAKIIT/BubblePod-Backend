from configparser import ConfigParser
import psycopg2
from typing import Dict


class bubbledb:
    def __init__(self):
        conn_info = self.initialize("db.ini")
        self.conn = psycopg2.connect(**conn_info)
        self.cur = self.conn.cursor()


    def initialize(ini_filename: str) -> Dict[str, str]:
        parser = ConfigParser()
        parser.read(ini_filename)
        # Create a dictionary of the variables stored under the "accounts" section of the .ini
        conn_info = {param[0]: param[1] for param in parser.items("accounts")}
        return conn_info


    def close(self):
        self.conn.close()
        self.cur.close()
    

    def execute_sql(self, query: str) -> None:
        try:
            self.cur.execute(query)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {self.cur.query}")
            self.conn.rollback()
            self.cur.close()
        else:
            self.conn.commit()

            
    def create_table(self) -> None:
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
        self.execute_sql(query)
    
    
    def insert(self, data) -> None:
        query = f"""
                    INSERT INTO accounts()
                    VALUES ({data[1]},
                            {data[2]},
                            {data[3]},
                            {data[4]},
                            {data[5]},
                            {data[6]},
                            {data[7]},
                            {data[8]};
                """
        self.execute_sql(query)

    
    def fetch(self):
        #logic needs to be implemented depending on how frontend calls for displaying user profiles will be
        pass


    def fetch_interests(self):
        query = f"""
                    SELECT interest1, interest2, interest3 FROM accounts
                """
        self.execute_sql(query)
        return self.cur.fetchall()




#This is a special function due to the way psql works
def create_db(conn_info = bubbledb.initialize()) -> None:
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

