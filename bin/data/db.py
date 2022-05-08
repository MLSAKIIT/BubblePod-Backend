from configparser import ConfigParser
import psycopg2
from typing import Dict
import sqlalchemy
import pandas as pd


class bubbledb:
    def __init__(self):
        conn_info = self.initialize()
        self.conn = psycopg2.connect(**conn_info)
        self.cur = self.conn.cursor()
        self.engine = sqlalchemy.create_engine('postgresql://postgres:password@localhost:5432/bubblepod')
        try:
            self.create_table()
        except:
            pass


    def initialize(self) -> Dict[str, str]:
        parser = ConfigParser()
        config = "app.ini"
        parser.read(config)
        conn_info = {param[0]: param[1] for param in parser.items("accounts")}
        return conn_info


    def close(self):
        self.conn.close()
        self.cur.close()
    

    def execute_sql(self, query: str) -> None:
        self.cur = self.conn.cursor() #reinitialise incase cursor is closed. 
        try:
            self.cur.execute(query)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {self.cur.query}")
            self.conn.rollback()
            self.cur.close()
        else:
            self.conn.commit()

            
    def create_main_table(self) -> None:
        query = """
                    CREATE TABLE IF NOT EXISTS accounts (
                    index serial PRIMARY KEY,
                    username VARCHAR(20) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    interest1 VARCHAR(50) NOT NULL,
                    interest2 VARCHAR(50) NOT NULL,
                    interest3 VARCHAR(50) NOT NULL,
                    cluster INT);
                """
        self.execute_sql(query)

    
    def create_db(self) -> None:
        # Connect just to PostgreSQL with the user loaded from the .ini file
        conn_info = self.initialize()
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

    
    def insert(self, table, data) -> None:
        if table == "accounts":
            query = f"""
                        INSERT INTO accounts (
                            username,
                            email,
                            interest1,
                            interest2,
                            interest3
                        )
                        VALUES ('{data[0]}',
                                '{data[1]}',
                                '{data[2]}',
                                '{data[3]}',
                                '{data[4]}');
                    """
        elif table == "clusters":
            query = f"""
                INSERT INTO clusters (cluster)
                VALUES ({data});
            """
        self.execute_sql(query)

    
    def fetch(self, username):
        query = f"""
                    SELECT cluster
                    FROM accounts
                    WHERE username = '{username}';        
                """
        self.execute_sql(query)
        return self.cur.fetchone()


    def fetch_interests(self):
        query = f"""
                    SELECT interest1, interest2, interest3 FROM accounts
                """
        self.execute_sql(query)
        return self.cur.fetchall()

    def dataframe_to_table(self, dataframe):
        dataframe.to_sql('accounts', self.engine, if_exists="replace", index=False)

    def table_to_dataframe(self, table):
        dataframe = pd.read_sql(table, self.engine)
        return dataframe



#Unit Testing
bubbledb = bubbledb()
print(bubbledb.table_to_dataframe("accounts").head())