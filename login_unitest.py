#login
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestLoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the WebDriver (e.g., Chrome)
        cls.driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

    def test_show_login_form(self):
        # Open the login page
        self.driver.get("file:///path/to/your/login.html")  # Replace with the actual path to your HTML file

        # Test resident button
        resident_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כתושב')]")
        resident_button.click()
        resident_form = self.driver.find_element(By.ID, "residentLoginForm")
        self.assertEqual(resident_form.value_of_css_property("display"), "block")

        # Test worker button
        worker_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כעובד')]")
        worker_button.click()
        worker_form = self.driver.find_element(By.ID, "workerLoginForm")
        self.assertEqual(worker_form.value_of_css_property("display"), "block")

        # Test admin button
        admin_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כמנהל')]")
        admin_button.click()
        admin_form = self.driver.find_element(By.ID, "adminLoginForm")
        self.assertEqual(admin_form.value_of_css_property("display"), "block")

    def test_handle_login(self):
        # Open the login page
        self.driver.get("file:///path/to/your/login.html")  # Replace with the actual path to your HTML file

        # Click the resident button and fill out the form
        resident_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כתושב')]")
        resident_button.click()

        username_input = self.driver.find_element(By.NAME, "residentUsername")
        password_input = self.driver.find_element(By.NAME, "residentPassword")
        login_button = self.driver.find_element(By.XPATH, "//form[@id='residentLoginForm']//button")

        username_input.send_keys("testUser")
        password_input.send_keys("testPassword")
        login_button.click()

        # Wait for the page to redirect
        time.sleep(2)  # Adjust the sleep time as needed

        # Check if the page was redirected to home.html
        self.assertIn("home.html", self.driver.current_url)

        # Check if the username and userType were saved in localStorage
        username = self.driver.execute_script("return localStorage.getItem('username');")
        user_type = self.driver.execute_script("return localStorage.getItem('userType');")
        self.assertEqual(username, "testUser")
        self.assertEqual(user_type, "resident")

    @classmethod
    def tearDownClass(cls):
        # Close the browser
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main() 

