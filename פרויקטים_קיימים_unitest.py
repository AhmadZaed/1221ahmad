import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestExistingProjectsPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the WebDriver (e.g., Chrome)
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
        cls.base_url = "file:///path/to/your/html/file.html"  # Update this path to your local HTML file

    def test_page_title(self):
        # Test if the page title is correct
        self.driver.get(self.base_url)
        self.assertEqual(self.driver.title, "פרויקטים קיימים")

    def test_navbar_links(self):
        # Test if the navbar links are present and functional
        self.driver.get(self.base_url)
        navbar_links = self.driver.find_elements(By.CLASS_NAME, "w3-bar-item")
        self.assertGreater(len(navbar_links), 0)  # Ensure there are navbar links

        # Test the "דף בית" link
        home_link = self.driver.find_element(By.LINK_TEXT, "דף בית")
        home_link.click()
        self.assertIn("home.html", self.driver.current_url)  # Verify the URL after clicking

    def test_projects_list(self):
        # Test if the projects list is displayed correctly
        self.driver.get(self.base_url)
        projects_list = self.driver.find_element(By.ID, "projects-list")
        self.assertTrue(projects_list.is_displayed())

        # Check if the "לא נמצאו פרויקטים" message appears when no projects are present
        no_projects_message = projects_list.find_elements(By.TAG_NAME, "p")
        if no_projects_message:
            self.assertIn("לא נמצאו פרויקטים", no_projects_message[0].text)

    def test_logout_button(self):
        # Test if the logout button works
        self.driver.get(self.base_url)
        logout_button = self.driver.find_element(By.CLASS_NAME, "logoutbtn")
        logout_button.click()
        time.sleep(2)  # Wait for the alert to appear
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "התנתקת בהצלחה!")
        alert.accept()
        self.assertIn("login.html", self.driver.current_url)  # Verify redirection to login page

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are done
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()