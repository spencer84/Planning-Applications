from SiteNavigator import SiteNavigator
from PlanningApplication import PlanningApplication
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from dbconnect import dbconnect
import datetime
import time

# Open a Chrome browser and navigate to the council planning page
# site = 'https://www.cheshirewestandchester.gov.uk/residents/planning-and-building-control/' \
#        'see-or-comment-on-planning-applications.aspx'

site = 'https://pa.cheshirewestandchester.gov.uk/online-applications/search.do?action=advanced'

# Get data from last week 
current_date = datetime.date.today()
start_date = current_date - datetime.timedelta(days = 7)
start_date = start_date.strftime("%d/%m/%Y")
end_date = current_date.strftime("%d/%m/%Y")
local_planning_authority = "Cheshire West and Chester"

# Connect to database
db = dbconnect()
db.connect()

class ApplicationNavigator(SiteNavigator):
    """
    Inherited from the SiteNavigator class, this class is designed specifically for parsing Planning Applications stored
    on a council's website.
    """
    def __init__(self):
        self.number_of_applications = 0

    def agree(self):
        """
        Agree to any terms/agreements that may be at the page
        :return: None
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ccc-reject-settings"]'))).click()

    def searchDecided(self, start_date = start_date, end_date = end_date):
        """
        Search decided applications by a given date range
        :return:
        """
        self.end_reached = False
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id=\"applicationDecisionStart\"]"))).send_keys(start_date)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id=\"applicationDecisionEnd\"]"))).send_keys(
                end_date)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/form/div[4]/input[2]'))).click()
        except selenium.common.exceptions.TimeoutException:
            return

        # Store the first page of results
        self.current_page = self.driver.current_url
        
    def searchSubmitted(self, start_date = start_date, end_date = end_date):
        """
        Search submitted applications by a given date range 
        """
        nav.end_reached = False
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id=\"applicationReceivedStart\"]"))).send_keys(start_date)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id=\"applicationReceivedEnd\"]"))).send_keys(
                end_date)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/form/div[4]/input[2]'))).click()
        except selenium.common.exceptions.TimeoutException:
            return

        # Store the first page of results
        self.current_page = self.driver.current_url

    def add_results(self):
        """For every search result on a page, visit each link, then parse content to a database"""
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@class=\'searchresult\']/a")))
        self.search_results = [element.get_attribute("href") for element in self.driver.find_elements(By.XPATH, "//*[@class=\'searchresult\']/a")]
        for link in self.search_results:
            self.driver.get(link)
            app = PlanningApplication()
            self.number_of_applications +=1
            app.link = link
            app.local_planning_authority = local_planning_authority
            # Get data here
            values = self.driver.find_elements(By.TAG_NAME, "td" )
            keys = self.driver.find_elements(By.TAG_NAME, "th")
            # Extract the text from the td/th elements (showing the descriptive values)
            key_array = [key.text for key in keys]
            value_array = [value.text for value in values]
            value_dict = dict(zip(key_array, value_array))
            # Assign attributes to the planning application based on array position
            print(value_dict)
            app.reference = value_dict.get('Reference')
            app.alt_reference = value_dict.get('Alternative Reference')
            app.date_received = datetime.datetime.strptime(value_dict.get('Application Received'), "%a %d %b %Y").strftime("%Y-%m-%d")
            app.address = value_dict.get('Address')
            # Need to handle special characters ('') in the proposal
            app.proposal = value_dict.get('Proposal')
            app.proposal = app.proposal.replace('\'', '')
            app.proposal = app.proposal.replace('\"', '')
            app.status = value_dict.get('Status')
            app.decision = value_dict.get('Decision')
            if value_dict.get('Decision Issued Date'): 
                app.decision_date = datetime.datetime.strptime(value_dict.get('Decision Issued Date'), "%a %d %b %Y").strftime("%Y-%m-%d")
            app.appeal = value_dict.get('Appeal Decision')
            app.appeal_status = value_dict.get('Appeal Status')
            app.date_collected = datetime.datetime.now().strftime("%Y-%m-%d")
            # Attempt to extract a postcode field
            app.get_postcode()
            print(app)
            # Send planning application to database
            app.sendToDatabase(db.connection)
            # Parse geo data and send to db
            app.getGeoData()
            app.sendGeoData(db.connection)
            # Parse proposal and send to nlp db
            app.lemmAndStem()
            app.sendNLP(db.connection)
            # Return to search result page
            self.driver.get(self.current_page)

    def next_page(self):
        try:
            next_page = self.driver.find_element(By.CLASS_NAME, "next").get_attribute('href')
            self.current_page = next_page
            self.driver.get(self.current_page)
        except selenium.common.exceptions.NoSuchElementException:
            self.end_reached = True
            

if __name__ == "__main__":
    nav = ApplicationNavigator()
    nav.site = site
    nav.open_page()
    some_time_ago = datetime.date(2022, 7, 7)
    one_week_later = some_time_ago+datetime.timedelta(days=7)
    some_time_ago = some_time_ago.strftime("%d/%m/%Y")
    one_week_later = one_week_later.strftime("%d/%m/%Y")
    # First search through the decided results
    nav.searchDecided()
    while not nav.end_reached:
        nav.add_results()
        nav.next_page()
        # Avoid 'Too Many Requests' error by waiting
        time.sleep(60)
    # # Then search through submitted results
    nav.searchSubmitted()
    while not nav.end_reached:
        nav.add_results()
        nav.next_page()
        # Avoid 'Too Many Requests' error by waiting
        time.sleep(60)
    print(f"Total number of applications added: {nav.number_of_applications}")
    db.connection.close()

    
