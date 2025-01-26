import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestAddProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # מאתחל את הדפדפן (במקרה הזה כרום)
        cls.driver = webdriver.Chrome()
        # מגדיר המתנה מרבית של 10 שניות לאיתור אלמנטים בדף
        cls.driver.implicitly_wait(10)
        # פותח את הקובץ HTML המקומי (יש להחליף את הנתיב לנתיב של הקובץ שלך)
        cls.driver.get("file:///path/to/your/html/file.html")

    @classmethod
    def tearDownClass(cls):
        # סוגר את הדפדפן לאחר סיום כל הבדיקות
        cls.driver.quit()

    def test_add_project(self):
        # בודק הוספת פרויקט חדש
        # ממלא את שדות הטופס
        self.driver.find_element(By.ID, "projectName").send_keys("פרויקט חדש")
        self.driver.find_element(By.ID, "projectDescription").send_keys("תיאור הפרויקט")
        self.driver.find_element(By.ID, "projectStatus").send_keys("בתכנון")
        self.driver.find_element(By.ID, "startDate").send_keys("2023-10-01")
        self.driver.find_element(By.ID, "endDate").send_keys("2023-12-31")

        # שולח את הטופס
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # מחכה להודעת האישור
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        # בודק אם ההודעה מכילה את הטקסט "הפרויקט הוסף בהצלחה!"
        self.assertIn("הפרויקט הוסף בהצלחה!", alert.text)
        alert.accept()

        # בודק אם הדף עבר לדף עדכון הפרויקטים
        self.assertIn("עדכון_פרויקטים_ויוזמות_עירוניות.html", self.driver.current_url)

    def test_cancel_form(self):
        # בודק ביטול הטופס
        # לוחץ על כפתור הביטול
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-cancel").click()

        # מחכה לאישור בחלון האלתור
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        # מאשר את הביטול
        alert.accept()

        # בודק אם הדף עבר לדף עדכון הפרויקטים
        self.assertIn("עדכון_פרויקטים_ויוזמות_עירוניות.html", self.driver.current_url)

if __name__ == "__main__":
    # מריץ את כל הבדיקות כאשר הקובץ מופעל
    unittest.main()