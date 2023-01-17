import re
import requests
import string
from nltk.stem import WordNetLemmatizer, SnowballStemmer

class PlanningApplication:
    def __init__(self):
        self.reference = None
        self.alt_reference = None
        self.date_received = None
        self.address = None
        self.proposal = None
        self.status = None
        self.decision = None
        self.decision_date = "9999-12-31"
        self.appeal = None
        self.appeal_status = None
        self.local_planning_authority = None
        self.date_collected = None
        self.postcode = None
        self.link = None
        # Additional geographic data
        self.region = None
        self.latitude = 0.0
        self.longitude = 0.0
        # Add processed text data
        self.proposal_parsed = []

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
            Link: {self.link}
            """
        )
            
        
    def sendToDatabase(self, connection):
        """Either update or insert new record"""
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO applications (ReferenceNumber, LocalPlanningAuthority, AlternativeReferenceNumber, DateReceived,
        Address, Proposal, Status, Decision, DecisionDate, Appeal, AppealStatus, DateDataRetrieved, Postcode, Link) values ('{self.reference}', '{self.local_planning_authority}','{self.alt_reference}',
        '{self.date_received}','{self.address}','{self.proposal}','{self.status}','{self.decision}','{self.decision_date}','{self.appeal}',
        '{self.appeal_status}', '{self.date_collected}', '{self.postcode}', '{self.link}')
        ON DUPLICATE KEY UPDATE DateDataRetrieved ='{self.date_collected}',
        Decision = '{self.decision}',
        DecisionDate = '{self.decision_date}', 
        Status = '{self.status}', 
        Appeal = '{self.appeal}', 
        AppealStatus = '{self.appeal_status}', 
        Link = '{self.link}'
        """)
        print("Successfully inserted row")
        connection.commit()

        """ Create table geo columns (ReferenceNumber, Postcode, Latitude, Longitude) )"""
    def getGeoData(self):
        """Request geodata from an application postcode"""
        if self.postcode:
            results = requests.get(f"https://api.postcodes.io/postcodes/{self.postcode}")
            results = results.json().get('result')
            try:
                self.region = results.get('region')
                self.latitude = results.get('latitude')
                self.longitude = results.get('longitude')
            except AttributeError as e:
                pass

    def sendGeoData(self, connection):
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO geo (ReferenceNumber, Latitude, Longitude) values ('{self.reference}', 
        '{self.latitude}', '{self.longitude}')""")

    def parseProposal(self):
        """Need to prepare proposal text for further analysis and transfer into an array format"""
        # Convert text to all lowercase
        if self.proposal:
            cleaned_text = self.proposal.lower()
        else:
            return
        # Remove punctuation
        cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))
        # Split string by spaces
        self.proposal_parsed = cleaned_text.split(" ")
    
    def lemmAndStem(self):
        """Apply Lemmation and Stemmation to the parsed text as a prelude"""
        lemmer = WordNetLemmatizer()
        stemmer = SnowballStemmer("english")
        self.proposal_lemm = [lemmer.lemmatize(x) for x in self.proposal_parsed]
        self.proposal_stem = [stemmer.stem(x) for x in self.proposal_lemm]
    
    def sendNLP(self, connection):
        """Send the processed proposal to the database"""
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO nlp (ReferenceNumber, Lemmation, Stemming) values ('{self.reference}', '{self.proposal_lemm}', '{self.proposal_stem}')""")



