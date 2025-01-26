import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCityImprovementIdeas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the WebDriver (e.g., Chrome)
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
        cls.driver.get("file:///path/to/your/html/file.html")  # Replace with the path to your HTML file

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()

    def test_submit_idea_form(self):
        # Test submitting the idea form
        idea_title = "New Park"
        description = "We need a new park in the neighborhood."
        name = "John Doe"
        email = "john.doe@example.com"

        # Fill out the form
        self.driver.find_element(By.ID, "idea-title").send_keys(idea_title)
        self.driver.find_element(By.ID, "description").send_keys(description)
        self.driver.find_element(By.ID, "name").send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(email)

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verify that the form submission was successful
        success_message = self.driver.find_element(By.CLASS_NAME, "success-message")
        self.assertTrue(success_message.is_displayed())
        self.assertEqual(success_message.text, "הפידבק נשלח בהצלחה! תודה על שיתוף הפעולה.")

    def test_logout_functionality(self):
        # Test the logout functionality
        logout_button = self.driver.find_element(By.CLASS_NAME, "logoutbtn")
        logout_button.click()

        # Verify that the user is logged out
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "התנתקת בהצלחה!")
        alert.accept()

        # Verify that the login overlay is displayed
        login_overlay = self.driver.find_element(By.ID, "loginOverlay")
        self.assertTrue(login_overlay.is_displayed())

if __name__ == "__main__":
    unittest.main()