import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDepartmentProfessionals(unittest.TestCase):
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

    def test_electricity_department(self):
        # Test the Electricity department
        self._test_department("electricity", ["יוסי כהן", "דנה לוי"])

    def test_transport_department(self):
        # Test the Transport department
        self._test_department("transport", ["מיכאל ברק", "עדי שמעון"])

    def test_water_department(self):
        # Test the Water department
        self._test_department("water", ["גיא צור", "מאיה סולומון"])

    def test_sports_department(self):
        # Test the Sports department
        self._test_department("sports", ["רון כהן", "אלונה רז"])

    def test_cleaning_department(self):
        # Test the Cleaning department
        self._test_department("cleaning", ["תמר מזרחי", "יואל שמש"])

    def test_development_department(self):
        # Test the Development department
        self._test_department("development", ["דוד ישראלי", "נועה עמית"])

    def _test_department(self, department, expected_names):
        # Helper function to test a department
        # Click the department button
        button = self.driver.find_element(By.XPATH, f"//button[contains(@onclick, \"{department}\")]")
        button.click()

        # Wait for the professionals list to update
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "professional"))
        )

        # Get the list of professionals displayed
        professionals = self.driver.find_elements(By.CLASS_NAME, "professional")
        self.assertEqual(len(professionals), len(expected_names))  # Check the number of professionals

        # Verify the names of the professionals
        for i, prof in enumerate(professionals):
            self.assertIn(expected_names[i], prof.text)  # Check if the name is in the displayed text

if __name__ == "__main__":
    unittest.main()