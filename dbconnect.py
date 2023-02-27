from creds import username, password
import mariadb
import dbinit

class dbconnect:
    def __init__(self):
        self.connection = None
        self.connect()
        # Establish the database connection
        self.cursor = self.connection.cursor()

    def connect(self):
        """Connect to a database using stored credentials"""
        try:
            self.connection = mariadb.connect(user = username, password = password, database = "planning")
            print("Successfully connected to MySQL database.")
        except Exception as e:
            print("Error connecting to MySQL database: "+ e.msg) 

    def importApplication(self, application):
        """Import the details of a planning application into the MySQL database"""
        self.cursor.execute()

    
    