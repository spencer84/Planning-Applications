from creds import username, password
import mysql.connect

class dbconnect:
    def __init__(self):
        self.connection = None
    def connect(username = username, password = password, host = "127.0.0.0"):
        """Connect to a database using stored credentials"""