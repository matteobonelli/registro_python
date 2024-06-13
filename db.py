import mysql.connector
from mysql.connector import Error
import configparser

config = configparser.ConfigParser()
config.read('dbConfig.ini')

class DBClass:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=config['db']['host'],
                database=config['db']['database'],
                user=config['db']['user'],
                password=config['db']['password'],
            )

        except Error as e:
            print(f"Error during connection{e}")

    def disconnect(self):
        if(self.connection) is not None and self.connection.is_connected():
            self.connection.close()
            print("MySql connection is closed")

    def execute_query(self, query):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columnNames = cursor.column_names
            return result, columnNames
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor is not None:
                cursor.close()

    def execute_procedure(self, procedure):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.callproc(procedure)
            result = cursor.fetchall()
            columnNames = cursor.column_names
            return result, columnNames
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor is not None:
                cursor.close()

