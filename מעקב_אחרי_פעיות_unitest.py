import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestReportTracking(unittest.TestCase):
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

    def test_update_status(self):
        # בודק עדכון סטטוס של דוח
        self._update_status(0, "בטיפול")  # מעדכן את הסטטוס של הדוח הראשון ל"בטיפול"
        updated_status = self.driver.find_element(By.XPATH, "//div[@class='report-item'][1]//p[contains(text(), 'סטטוס נוכחי')]")
        self.assertIn("בטיפול", updated_status.text)  # בודק אם הסטטוס התעדכן בהצלחה

    def test_set_priority(self):
        # בודק עדכון עדיפות של דוח
        self._set_priority(0, 1)  # מעדכן את העדיפות של הדוח הראשון ל"גבוהה"
        updated_priority = self.driver.find_element(By.XPATH, "//div[@class='report-item'][1]//span[@class='priority']")
        self.assertEqual(updated_priority.text, "גבוהה")  # בודק אם העדיפות התעדכנה בהצלחה

    def test_delete_report(self):
        # בודק מחיקת דוח
        initial_reports_count = len(self.driver.find_elements(By.CLASS_NAME, "report-item"))
        self._delete_report(0)  # מוחק את הדוח הראשון
        updated_reports_count = len(self.driver.find_elements(By.CLASS_NAME, "report-item"))
        self.assertEqual(updated_reports_count, initial_reports_count - 1)  # בודק אם הדוח נמחק

    def test_subscribe_for_notifications(self):
        # בודק הרשמה להתראות
        self._subscribe_for_notifications(0)  # נרשם להתראות עבור הדוח הראשון
        alert = self.driver.switch_to.alert  # עובר לחלון האלתור
        self.assertIn("נרשמת לקבלת התראות", alert.text)  # בודק את הטקסט בהודעה
        alert.accept()  # סוגר את חלון האלתור

    def _update_status(self, index, new_status):
        # פונקציה עזר לעדכון סטטוס של דוח
        status_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), '{new_status}')]")
        status_button.click()

    def _set_priority(self, index, priority):
        # פונקציה עזר לעדכון עדיפות של דוח
        priority_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), 'עדיפות {self._get_priority_text(priority)}')]")
        priority_button.click()

    def _delete_report(self, index):
        # פונקציה עזר למחיקת דוח
        delete_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(@class, 'red')]")
        delete_button.click()
        # מאשר את המחיקה בחלון האלתור
        alert = self.driver.switch_to.alert
        alert.accept()

    def _subscribe_for_notifications(self, index):
        # פונקציה עזר להרשמה להתראות
        subscribe_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), 'קבלת התראות')]")
        subscribe_button.click()

    def _get_priority_text(self, priority):
        # מחזיר את הטקסט המתאים לעדיפות
        if priority == 1:
            return "גבוהה"
        elif priority == 2:
            return "בינונית"
        elif priority == 3:
            return "נמוכה"
        return "לא הוגדרה"

if __name__ == "__main__":
    # מריץ את כל הבדיקות כאשר הקובץ מופעל
    unittest.main()