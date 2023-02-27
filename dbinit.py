from creds import username, password
import mariadb

# Initialise the databases

def createApplicationDatabase(cursor):
    # Main application database
    query = """ 
    CREATE TABLE IF NOT EXISTS applications 
    (ReferenceNumber text, LocalPlanningAuthority text, AlternativeReferenceNumber text,
    DateReceived date, Address text, Proposal text, Status text, Decision text, DecisionDate text,
    Appeal text, AppealStatus text, DateDataRetrieved date, Postcode text, Link text);
    """
    cursor.execute(query)
    return

def createGeoDatabase(cursor):
    # Database for geographic data
    query = """ 
    CREATE TABLE IF NOT EXISTS geo (ReferenceNumber text, Postcode text, Latitude text, Longitude text);
    """
    cursor.execute(query)
    return
