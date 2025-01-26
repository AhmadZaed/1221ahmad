import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestWebApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (assuming Chrome here)
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

    def test_home_page_loads(self):
        # Open the home page
        self.driver.get("http://yourwebsite.com/home.html")
        # Check if the title is correct
        self.assertIn("דף בית", self.driver.title)

    def test_navigation_to_report_hazard(self):
        # Open the home page
        self.driver.get("http://yourwebsite.com/home.html")
        # Find the link to the hazard reporting page and click it
        self.driver.find_element(By.LINK_TEXT, "דיווח על מפגעים").click()
        # Check if the title is correct
        self.assertIn("דיווח על מפגעים", self.driver.title)

    @classmethod
    def tearDownClass(cls):
        # Close the browser
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()