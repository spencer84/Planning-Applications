from SiteNavigator import SiteNavigator
from PlanningApplication import PlanningApplication
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Open a Chrome browser and navigate to the council planning page
# site = 'https://www.cheshirewestandchester.gov.uk/residents/planning-and-building-control/' \
#        'see-or-comment-on-planning-applications.aspx'

site = 'https://pa.cheshirewestandchester.gov.uk/online-applications/search.do?action=advanced'

# Eventually have these reflect the most recent record to the current date.
start_date = '01/07/2022'
end_date = '08/07/2022'
local_planning_authority = "Cheshire West and Chester"



class ApplicationNavigator(SiteNavigator):
    """
    Inherited from the SiteNavigator class, this class is designed specifically for parsing Planning Applications stored
    on a council's website.
    """
    def agree(self):
        """
        Agree to any terms/agreements that may be at the page
        :return: None
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ccc-reject-settings"]'))).click()

    def search(self):
        """
        Search by a given date range
        :return:
        """
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"applicationDecisionStart\"]"))).send_keys(start_date)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"applicationDecisionEnd\"]"))).send_keys(
            end_date)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/form/div[4]/input[2]'))).click()

        # Store the first page of results
        self.current_page = self.driver.current_url
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@class=\'searchresult\']/a")))
        self.search_results = [element.get_attribute("href") for element in self.driver.find_elements(By.XPATH, "//*[@class=\'searchresult\']/a")]
        print(self.search_results)


    def add_results(self):
        """For every search result on a page, visit each link, then parse content to a database"""
        for link in self.search_results:
            self.driver.get(link)
            app = PlanningApplication()
            app.local_planning_authority = local_planning_authority
            # Get data here
            values = self.driver.find_elements(By.TAG_NAME, "td" )
            # Extract the text from the td elements (showing the descriptive values)
            value_array = [value.text for value in values]
            # Assign attributes to the planning application based on array position
            app.reference = value_array[0]
            app.alt_reference = value_array[1]
            app.date_received = value_array[2]
            app.address = value_array[3]
            app.proposal = value_array[4]
            app.status = value_array[5]
            app.decision = value_array[6]
            app.decision_date = value_array[7]
            app.appeal = value_array[8] 
            app.appeal_status = value_array[9]
            app.printAttributes()
            # Return to search result page
            self.driver.get(self.current_page)

    # def next_page(self):
    #
    #
    #
    #
    # def find_apps(self):
    #     """
    #
    #     :return:
    #     """


if __name__ == "__main__":
    nav = ApplicationNavigator()
    nav.site = site
    nav.open_page()
    nav.search()
    nav.add_results()
    
