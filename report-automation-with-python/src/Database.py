import pyodbc
import os


class DatabaseQuery:
    def __init__(self, connection):
        self.cursor = None
        self.connection = None

    def database_connection(self, server, database, port, user, password, driver):
        """
        Establish database connection
        """
        try:
            self.connection = pyodbc.connect(f"DRIVER={driver};SERVER=tcp:{server};PORT={port};DATABASE={database};"
                                            f"UID={user};PWD={password}")
        except pyodbc.Error as err:


    def database_cursor(self, connection):

