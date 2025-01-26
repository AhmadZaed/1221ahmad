import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestAddModuleForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (Chrome in this case)
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load
        cls.driver.get("http://yourwebsite.com/add_module.html")  # Replace with your actual URL

    def test_form_submission(self):
        # Test the form submission with valid data
        driver = self.driver

        # Find the input field and enter a module name
        module_input = driver.find_element(By.ID, "newModuleName")
        module_input.send_keys("New Module Test")

        # Find and click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Check if the alert is displayed with the correct message
        alert = driver.switch_to.alert
        self.assertIn("המודול \"New Module Test\" נוסף בהצלחה!", alert.text)
        alert.accept()  # Close the alert

        # Check if the input field is reset
        self.assertEqual(module_input.get_attribute("value"), "")

    def test_form_validation(self):
        # Test form validation (e.g., empty input)
        driver = self.driver

        # Find and click the submit button without entering any data
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Check if the input field is marked as required (HTML5 validation)
        module_input = driver.find_element(By.ID, "newModuleName")
        self.assertTrue(module_input.get_attribute("required"))

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()

if __name__ == "__main__":
    # Run the tests
    unittest.main()