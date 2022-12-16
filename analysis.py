
from dbconnect import dbconnect
# Perform additional analysis on the Planning applications

# 1. Geo-locate 
#   - parse address field to extract a postcode if possible
db = dbconnect()
db.connection.cursor()
#   - functionality to identify exact location of application 
#   - Nearby postcodes

# Create a table for more address details (i.e postcode, lat/long, etc)

# 2. Build NLP Model to interpret the type of application

# 3. Build database of appeals records

# 4. Extrapolate number of housing units proposed