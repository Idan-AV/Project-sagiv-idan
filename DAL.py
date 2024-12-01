import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DAL:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user= os.getenv("DB_USER"),
                password= os.getenv("DB_PASSWORD"),
                database= os.getenv("DB_DATABASE"),
                autocommit=True
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.connection = None

    def validate_query_params(self, query, params):
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if params is not None and not isinstance(params, tuple):
            raise ValueError("Params must be a tuple")

    def execute_query(self, query, params=None, fetchall=False, fetchone=False):
        self.validate_query_params(query, params)
        if self.connection:
            try:
                with self.connection.cursor(dictionary=True) as cursor:
                    print(f"Executing query: {query}")
                    if params:
                        print(f"With parameters: {params}")
                        cursor.execute(query, params)
                        if fetchall:
                            result = cursor.fetchall()
                            print(f"Fetched {len(result)} rows")
                            return result
                        elif fetchone:
                            result = cursor.fetchone()
                            print(f"Fetched one row")
                            return result
                        else:
                            print(f"query affected {cursor.rowcount} rows")
                        return cursor

            except mysql.connector.Error as err:
                print(f"Error executing query: {query}")
        return None

    def get_table(self, query, params=None):
        return self.execute_query(query, params, fetchall=True)

    def get_scalar(self, query, params=None):
        return self.execute_query(query, params, fetchone=True)

    def insert(self, query, params=None):
        return self.execute_query(query, params)

    def delete(self, query, params=None):
        return self.execute_query(query, params)

    def update(self, query, params=None):
        return self.execute_query(query, params)

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.close()
            print("Connection close.")


if __name__ == "__main__":
    with DAL() as dal:
        print("\n===get table example===")
        # countries = dal.get_table("SELECT * FROM countries where population > %s", (0,))
        countries = dal.get_table("SELECT * FROM countries")
        users = dal.get_table("SELECT * FROM users where age > %s", (25, ))
        

        for country in countries:
            print(f"Country name: {country['name']}")
        
        for user in users:
            print(f"User name: {user['name']}, age: {user['age']}")
