import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestActivityTracking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (Chrome in this case)
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load
        cls.driver.get("http://yourwebsite.com/מעקב_אחרי_פעיות.html")  # Replace with your actual URL

    def test_table_display(self):
        # Test if the table displays the correct data
        driver = self.driver

        # Find the table rows
        table_rows = driver.find_elements(By.CSS_SELECTOR, "#reports-table-body tr")

        # Check if the number of rows matches the number of reports
        self.assertEqual(len(table_rows), 3)

        # Check the content of the first row
        first_row = table_rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(first_row[0].text, "דוח 1")
        self.assertEqual(first_row[1].text, "ממתין")
        self.assertEqual(first_row[2].text, "גבוהה")

    def test_map_markers(self):
        # Test if the map displays the correct markers
        driver = self.driver

        # Find the map container
        map_container = driver.find_element(By.ID, "map")

        # Check if the map is displayed
        self.assertTrue(map_container.is_displayed())

        # Check if the map has markers (this is a basic check, more advanced checks can be added)
        # Note: Selenium cannot directly interact with Leaflet.js markers, so this is a placeholder
        # for more advanced testing using JavaScript execution.
        markers = driver.execute_script("return document.querySelectorAll('.leaflet-marker-icon').length;")
        self.assertGreater(markers, 0)

    def test_navigation(self):
        # Test if the navigation bar works correctly
        driver = self.driver

        # Find and click the "דף בית" link
        home_link = driver.find_element(By.LINK_TEXT, "דף בית")
        home_link.click()

        # Check if the page navigates to the home page
        self.assertIn("home.html", driver.current_url)

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()

if __name__ == "__main__":
    # Run the tests
    unittest.main()