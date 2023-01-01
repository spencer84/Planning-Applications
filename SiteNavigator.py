from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

class SiteNavigator:
    """
    A class to navigate and parse the contents of a given website.
    """
    def __init__(self):
        self.site = None
        self.driver = None
        self.current_page = None
        self.search_results = []
        self.end_reached = False

    def open_page(self):
        """
        Attempt to return to the given site using the webdriver object from Selenium
        :return: driver object opened to the site
        """
        driver = webdriver.Chrome("chromedriver", options=chrome_options) # Need to store the chromedriver file to local directory
        driver.get(self.site)
        # There may be some commonalities across different types of planning pages;
        # Perhaps in the future this function could also identify whether a given site fits into any previously
        # observed patterns for a planning application website.
        self.driver = driver

