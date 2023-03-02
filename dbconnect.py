from creds import username, password
import mariadb

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
        return
    def queryJSON(self, query):
        """Query the database and return a result in JSON format"""
        self.cursor.execute(query)
        r = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]
        return {'results':r}