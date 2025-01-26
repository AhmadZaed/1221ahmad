import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestReportForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (Chrome in this case)
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load
        cls.driver.get("http://yourwebsite.com/דיווח על מפגעים.html")  # Replace with your actual URL

    def test_form_submission(self):
        # Test the form submission with valid data
        driver = self.driver

        # Fill in the description
        description = driver.find_element(By.ID, "description")
        description.send_keys("תיאור מפגע לדוגמה")

        # Select priority
        priority = driver.find_element(By.ID, "priority")
        priority.send_keys("גבוהה")

        # Interact with the map (click to set a marker)
        map_element = driver.find_element(By.ID, "map")
        action = webdriver.ActionChains(driver)
        action.move_to_element(map_element).click().perform()

        # Upload an image
        image_input = driver.find_element(By.ID, "image-upload")
        image_input.send_keys("/path/to/your/test/image.jpg")  # Replace with a valid image path

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
        submit_button.click()

        # Check if the form submission was successful
        time.sleep(2)  # Wait for the page to redirect
        self.assertIn("track_reports.html", driver.current_url)

    def test_form_validation(self):
        # Test form validation (e.g., missing required fields)
        driver = self.driver

        # Try to submit the form without filling in any fields
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
        submit_button.click()

        # Check if an alert is shown for missing fields
        alert = driver.switch_to.alert
        self.assertIn("יש להעלות תמונה", alert.text)
        alert.accept()

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()