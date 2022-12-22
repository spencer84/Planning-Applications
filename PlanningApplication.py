import re
import requests

class PlanningApplication:
    def __init__(self):
        self.reference = None
        self.alt_reference = None
        self.date_received = None
        self.address = None
        self.proposal = None
        self.status = None
        self.decision = None
        self.decision_date = None
        self.appeal = None
        self.appeal_status = None
        self.local_planning_authority = None
        self.date_collected = None
        self.postcode = None
        # Additional geographic data
        self.region = None
        self.latitude = None
        self.longitude = None

    def get_postcode(self):
        """ Use a regular expression to parse the address field and extract a postcode """   
        postcode = re.findall("([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})", self.address)
        if postcode:
            self.postcode = postcode[0][1]

    def __repr__(self):
        return(
            f"""
            Reference Number: {self.reference} 
            Local Planning Authority: {self.local_planning_authority}
            Alternative Ref Number: {self.alt_reference}
            Date Received: {self.date_received}
            Address: {self.address}
            Postcode: {self.postcode}
            Proposal: {self.proposal}
            Status: {self.status}
            Decision: {self.decision}
            Decision Date: {self.decision_date}
            Appeal: {self.appeal}
            Appeal Status: {self.appeal_status}
            """
        )
            
        
    def sendToDatabase(self, connection):
        """Either update or insert new record"""
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO applications (ReferenceNumber, LocalPlanningAuthority, AlternativeReferenceNumber, DateReceived,
        Address, Proposal, Status, Decision, DecisionDate, Appeal, AppealStatus, DateDataRetrieved, Postcode) values ('{self.reference}', '{self.local_planning_authority}','{self.alt_reference}',
        '{self.date_received}','{self.address}','{self.proposal}','{self.status}','{self.decision}','{self.decision_date}','{self.appeal}',
        '{self.appeal_status}', '{self.date_collected}', '{self.postcode}')
        ON DUPLICATE KEY UPDATE DateDataRetrieved ='{self.date_collected}'""")
        print("Successfully inserted row")
        connection.commit()

        """ Create table geo columns (ReferenceNumber, Postcode, Latitude, Longitude) )"""
    def getGeoData(self):
        """Request geodata from an application postcode"""
        if self.postcode:
            results = requests.get(f"https://api.postcodes.io/postcodes/{self.postcode}")
            results = results.json().get('result')
            self.region = results.get('region')
            self.latitude = results.get('latitude')
            self.longitude = results.get('longitude')

    def sendGeoData(self, connection):
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO geo (ReferenceNumber, Latitude, Longitude) values ('{self.reference}'""")

