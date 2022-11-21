from creds import username, password
import mariadb

class dbconnect:
    def __init__(self):
        self.connection = self.connect()
        # Establish the database connection
        self.cursor = self.connection.cursor()

    def connect(self):
        """Connect to a database using stored credentials"""
        print(f"Attempting to connect using username {username} and password {password}")
        try:
            self.connection = mariadb.connect(user = username, host ='127.0.0.1', port = 3306,  password = password, database = "planning")
            print("Successfully connected to MySQL database.")
        except Exception as e:
            print("Error connecting to MySQL database: "+ e.msg) 

    def importApplication(self, application):
        """Import the details of a planning application into the MySQL database"""
        self.cursor.execute()

if __name__ == "__main__":
    print("testing...")
    test = dbconnect()
    
    