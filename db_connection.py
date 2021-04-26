import os
import pyodbc
from configparser import ConfigParser


class DataComparison:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('db_connection.ini')

    def return_db_connection(self, db_name: str):
        return pyodbc.connect(
            f"Driver={self.config.get(db_name, 'Driver')}"
            f"Server={self.config.get(db_name, 'Server')}"
            f"Database={self.config.get(db_name, 'Database')}"
            f"Trusted_Connection={self.config.get(db_name, 'Trusted_Connection')}",
            timeout=3)
