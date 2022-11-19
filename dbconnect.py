from creds import username, password
import mysql.connector
from mysql.connector import Error

class dbconnect:
    def __init__(self):
        self.connection = None
        # Establish the database connection
        self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        """Connect to a database using stored credentials"""
        try:
            self.connection = mysql.connector.connect(username = username, password = password, host = "127.0.0.0", database = "planning")
            if self.connection.is_connected():
                print("Successfully connected to MySQL database.")
        except Error as e:
            print("Error connecting to MySQL database: "+ e.msg)
    def importApplication(self, application):
        """Import the details of a planning application into the MySQL database"""
        self.cursor.execute()
    