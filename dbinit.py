from creds import username, password
import mariadb

# Initialise the databases

def createApplicationDatabase(cursor):
    
    query = """ 
    CREATE TABLE applications IF NOT EXISTS applications 
    (ReferenceNumber text, LocalPlanningAuthority text, AlternativeReferenceNumber text,
    DateReceived date, Address text, Proposal text, Status text, Decision text, DecisionDate text,
    Appeal text, AppealStatus text, DateDataRetrieved date, Postcode text, Link text);
    """
    cursor.execute(query)
    return

def createGeoDatabase(cursor)
