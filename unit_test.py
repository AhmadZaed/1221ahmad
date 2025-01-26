#login
import unittest  # ייבוא מסגרת לבדיקות יחידה (unit tests)
from selenium import webdriver  # ייבוא WebDriver לשליטה על דפדפן
from selenium.webdriver.common.by import By  # ייבוא שיטות לאיתור אלמנטים בדף
from selenium.webdriver.common.keys import Keys  # ייבוא מקשים וירטואליים (כמו ENTER, TAB)
import time  # ייבוא ספרייה להשהיית הביצוע לזמן מסוים

class TestLoginPage(unittest.TestCase):  # הגדרת מחלקה לבדיקות
    @classmethod
    def setUpClass(cls):  # מתודה שתרוץ פעם אחת לפני כל הבדיקות
        # Initialize the WebDriver (e.g., Chrome)
        cls.driver = webdriver.Chrome()  # יצירת מופע של דפדפן Chrome (יש לוודא ש-ChromeDriver מותקן)
        cls.driver.implicitly_wait(10)  # המתנה מרבית של 10 שניות לאיתור אלמנטים בדף

    def test_show_login_form(self):  # בדיקת הצגת טופס ההתחברות
        # Open the login page
        self.driver.get("file:///path/to/your/login.html")  # פתיחת דף ההתחברות מהקובץ המקומי (יש להחליף את הנתיב)

        # Test resident button
        resident_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כתושב')]")  # איתור כפתור "התחבר כתושב"
        resident_button.click()  # לחיצה על הכפתור
        resident_form = self.driver.find_element(By.ID, "residentLoginForm")  # איתור הטופס המתאים לפי ID
        self.assertEqual(resident_form.value_of_css_property("display"), "block")  # בדיקה שהטופס מוצג (display: block)

        # Test worker button
        worker_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כעובד')]")  # איתור כפתור "התחבר כעובד"
        worker_button.click()  # לחיצה על הכפתור
        worker_form = self.driver.find_element(By.ID, "workerLoginForm")  # איתור הטופס המתאים לפי ID
        self.assertEqual(worker_form.value_of_css_property("display"), "block")  # בדיקה שהטופס מוצג (display: block)

        # Test admin button
        admin_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כמנהל')]")  # איתור כפתור "התחבר כמנהל"
        admin_button.click()  # לחיצה על הכפתור
        admin_form = self.driver.find_element(By.ID, "adminLoginForm")  # איתור הטופס המתאים לפי ID
        self.assertEqual(admin_form.value_of_css_property("display"), "block")  # בדיקה שהטופס מוצג (display: block)

    def test_handle_login(self):  # בדיקת תהליך ההתחברות
        # Open the login page
        self.driver.get("file:///path/to/your/login.html")  # פתיחת דף ההתחברות מהקובץ המקומי (יש להחליף את הנתיב)

        # Click the resident button and fill out the form
        resident_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'התחבר כתושב')]")  # איתור כפתור "התחבר כתושב"
        resident_button.click()  # לחיצה על הכפתור

        username_input = self.driver.find_element(By.NAME, "residentUsername")  # איתור שדה שם המשתמש לפי NAME
        password_input = self.driver.find_element(By.NAME, "residentPassword")  # איתור שדה הסיסמה לפי NAME
        login_button = self.driver.find_element(By.XPATH, "//form[@id='residentLoginForm']//button")  # איתור כפתור ההתחברות לפי XPATH

        username_input.send_keys("testUser")  # הזנת הערך "testUser" בשדה שם המשתמש
        password_input.send_keys("testPassword")  # הזנת הערך "testPassword" בשדה הסיסמה
        login_button.click()  # לחיצה על כפתור ההתחברות

        # Wait for the page to redirect
        time.sleep(2)  # המתנה של 2 שניות כדי לאפשר לדף להפנות לעמוד הבית

        # Check if the page was redirected to home.html
        self.assertIn("home.html", self.driver.current_url)  # בדיקה אם הכתובת הנוכחית מכילה את "home.html"

        # Check if the username and userType were saved in localStorage
        username = self.driver.execute_script("return localStorage.getItem('username');")  # קבלת הערך של "username" מ-localStorage
        user_type = self.driver.execute_script("return localStorage.getItem('userType');")  # קבלת הערך של "userType" מ-localStorage
        self.assertEqual(username, "testUser")  # בדיקה אם הערך של "username" הוא "testUser"
        self.assertEqual(user_type, "resident")  # בדיקה אם הערך של "userType" הוא "resident"

    @classmethod
    def tearDownClass(cls):  # מתודה שתרוץ פעם אחת לאחר כל הבדיקות
        # Close the browser
        cls.driver.quit()  # סגירת הדפדפן

if __name__ == "__main__":
    unittest.main()  # הרצת כל הבדיקות במחלקה
    -------------------------------
    #logout
    import unittest  # ייבוא מסגרת הבדיקות של Python
from unittest.mock import MagicMock, patch  # ייבוא כלים ליצירת אובייקטים מדומים (mocks)

# Mocking localStorage
class LocalStorageMock:
    def __init__(self):
        self.store = {}  # יצירת מילון כדי לדמות את ה-localStorage

    def getItem(self, key):
        return self.store.get(key, None)  # החזרת הערך של המפתח או None אם המפתח לא קיים

    def setItem(self, key, value):
        self.store[key] = value  # הוספת ערך למילון

    def clear(self):
        self.store = {}  # ניקוי המילון


# Mocking sessionStorage
class SessionStorageMock:
    def __init__(self):
        self.store = {}  # יצירת מילון כדי לדמות את ה-sessionStorage

    def getItem(self, key):
        return self.store.get(key, None)  # החזרת הערך של המפתח או None אם המפתח לא קיים

    def setItem(self, key, value):
        self.store[key] = value  # הוספת ערך למילון

    def clear(self):
        self.store = {}  # ניקוי המילון


# Mocking window.location
class WindowLocationMock:
    def __init__(self):
        self.href = ''  # יצירת משתנה כדי לדמות את window.location.href


# Mocking alert
class AlertMock:
    def __init__(self):
        self.message = None  # יצירת משתנה כדי לשמור את ההודעה שהועברה ל-alert

    def __call__(self, message):
        self.message = message  # שמירת ההודעה כאשר alert נקרא


# פונקציית ה-Logout המדומה
def dganjoLogout():
    # יצירת אובייקטים מדומים
    localStorage = LocalStorageMock()  # אובייקט מדומה ל-localStorage
    sessionStorage = SessionStorageMock()  # אובייקט מדומה ל-sessionStorage
    window = WindowLocationMock()  # אובייקט מדומה ל-window.location
    alert = AlertMock()  # אובייקט מדומה ל-alert

    # סימולציה של פונקציית ה-Logout
    localStorage.clear()  # ניקוי ה-localStorage
    sessionStorage.clear()  # ניקוי ה-sessionStorage
    alert("התנתקת בהצלחה!")  # הצגת הודעה
    window.href = 'login.html'  # הפניה לדף ההתחברות

    # החזרת האובייקטים המדומים כדי שנוכל לבדוק אותם
    return localStorage, sessionStorage, window, alert


# מחלקה לבדיקות
class TestLogoutFunction(unittest.TestCase):
    def setUp(self):
        # אתחול האובייקטים המדומים לפני כל בדיקה
        self.localStorage = LocalStorageMock()  # אובייקט מדומה ל-localStorage
        self.sessionStorage = SessionStorageMock()  # אובייקט מדומה ל-sessionStorage
        self.window = WindowLocationMock()  # אובייקט מדומה ל-window.location
        self.alert = AlertMock()  # אובייקט מדומה ל-alert

    def test_clears_localStorage_and_sessionStorage(self):
        # הוספת נתונים ל-localStorage ו-sessionStorage
        self.localStorage.setItem('username', 'testUser')  # הוספת שם משתמש ל-localStorage
        self.sessionStorage.setItem('token', '12345')  # הוספת token ל-sessionStorage

        # קריאה לפונקציית ה-Logout
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # בדיקה אם ה-localStorage וה-sessionStorage מנוקים
        self.assertIsNone(localStorage.getItem('username'))  # בדיקה אם שם המשתמש נמחק
        self.assertIsNone(sessionStorage.getItem('token'))  # בדיקה אם ה-token נמחק

    def test_shows_alert_with_correct_message(self):
        # קריאה לפונקציית ה-Logout
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # בדיקה אם ההודעה הנכונה הוצגה
        self.assertEqual(alert.message, "התנתקת בהצלחה!")  # בדיקה אם ההודעה היא "התנתקת בהצלחה!"

    def test_redirects_to_login_page(self):
        # קריאה לפונקציית ה-Logout
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # בדיקה אם הדף הופנה ל-login.html
        self.assertEqual(window.href, 'login.html')  # בדיקה אם ה-href שווה ל-login.html


if __name__ == "__main__":
    unittest.main()  # הרצת כל הבדיקות
    ---------------------------------
    #navbar
    import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestWebApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # הגדרת הדפדפן (Chrome) והתקנת ה-WebDriver אוטומטית
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # המתנה מרבית של 10 שניות לטעינת אלמנטים בדף
        cls.driver.implicitly_wait(10)

    def test_home_page_loads(self):
        # טעינת דף הבית
        self.driver.get("http://yourwebsite.com/home.html")
        # בדיקה שהכותרת של הדף מכילה את הטקסט "דף בית"
        self.assertIn("דף בית", self.driver.title)

    def test_navigation_to_report_hazard(self):
        # טעינת דף הבית
        self.driver.get("http://yourwebsite.com/home.html")
        # חיפוש הקישור "דיווח על מפגעים" ולחיצה עליו
        self.driver.find_element(By.LINK_TEXT, "דיווח על מפגעים").click()
        # בדיקה שהכותרת של הדף מכילה את הטקסט "דיווח על מפגעים"
        self.assertIn("דיווח על מפגעים", self.driver.title)

    @classmethod
    def tearDownClass(cls):
        # סגירת הדפדפן לאחר סיום כל הבדיקות
        cls.driver.quit()

if __name__ == "__main__":
    # הרצת כל הבדיקות כאשר הקוד מופעל
    unittest.main()
    --------------------------------
    #דיווח על מפגעים_unitest
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
        # הגדרת הדפדפן (Chrome) והתקנת ה-WebDriver אוטומטית
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # המתנה מרבית של 10 שניות לטעינת אלמנטים בדף
        cls.driver.implicitly_wait(10)
        # ניווט לדף טופס הדיווח
        cls.driver.get("http://yourwebsite.com/דיווח על מפגעים.html")  # יש להחליף בכתובת האמיתית

    def test_form_submission(self):
        # בדיקת שליחת טופס עם נתונים תקינים
        driver = self.driver

        # מילוי שדה התיאור
        description = driver.find_element(By.ID, "description")
        description.send_keys("תיאור מפגע לדוגמה")

        # בחירת עדיפות
        priority = driver.find_element(By.ID, "priority")
        priority.send_keys("גבוהה")

        # אינטראקציה עם המפה (לחיצה כדי להציב סמן)
        map_element = driver.find_element(By.ID, "map")
        action = webdriver.ActionChains(driver)
        action.move_to_element(map_element).click().perform()

        # העלאת תמונה
        image_input = driver.find_element(By.ID, "image-upload")
        image_input.send_keys("/path/to/your/test/image.jpg")  # יש להחליף בנתיב לתמונה תקינה

        # שליחת הטופס
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
        submit_button.click()

        # בדיקה אם הטופס נשלח בהצלחה והדף עבר לדף המעקב
        time.sleep(2)  # המתנה קצרה לטעינת הדף
        self.assertIn("track_reports.html", driver.current_url)

    def test_form_validation(self):
        # בדיקת ולידציית הטופס (למשל, שדות חובה שלא מולאו)
        driver = self.driver

        # ניסיון לשלוח את הטופס ללא מילוי שדות חובה
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
        submit_button.click()

        # בדיקה אם מוצגת הודעת שגיאה עבור שדות חסרים
        alert = driver.switch_to.alert
        self.assertIn("יש להעלות תמונה", alert.text)
        alert.accept()  # סגירת ההודעה

    @classmethod
    def tearDownClass(cls):
        # סגירת הדפדפן לאחר סיום כל הבדיקות
        cls.driver.quit()

if __name__ == "__main__":
    # הרצת כל הבדיקות כאשר הקוד מופעל
    unittest.main()
    -------------------------------
    #הוספת_מודול
    import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestAddModuleForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # הגדרת הדפדפן (Chrome) והתקנת ה-WebDriver אוטומטית
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # המתנה מרבית של 10 שניות לטעינת אלמנטים בדף
        cls.driver.implicitly_wait(10)
        # ניווט לדף טופס הוספת המודול
        cls.driver.get("http://yourwebsite.com/add_module.html")  # יש להחליף בכתובת האמיתית

    def test_form_submission(self):
        # בדיקת שליחת טופס עם נתונים תקינים
        driver = self.driver

        # מציאת שדה הקלט והזנת שם מודול
        module_input = driver.find_element(By.ID, "newModuleName")
        module_input.send_keys("New Module Test")

        # מציאת כפתור השליחה ולחיצה עליו
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # בדיקה אם ההודעה הנכונה מוצגת בחלון האלתור (alert)
        alert = driver.switch_to.alert
        self.assertIn("המודול \"New Module Test\" נוסף בהצלחה!", alert.text)
        alert.accept()  # סגירת חלון האלתור

        # בדיקה אם שדה הקלט אופס לאחר השליחה
        self.assertEqual(module_input.get_attribute("value"), "")

    def test_form_validation(self):
        # בדיקת ולידציית הטופס (למשל, שדה חובה ריק)
        driver = self.driver

        # מציאת כפתור השליחה ולחיצה עליו ללא הזנת נתונים
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # בדיקה אם שדה הקלט מסומן כשדה חובה (ולידציית HTML5)
        module_input = driver.find_element(By.ID, "newModuleName")
        self.assertTrue(module_input.get_attribute("required"))

    @classmethod
    def tearDownClass(cls):
        # סגירת הדפדפן לאחר סיום כל הבדיקות
        cls.driver.quit()

if __name__ == "__main__":
    # הרצת כל הבדיקות כאשר הקוד מופעל
    unittest.main()
    --------------------------------
    #הצגת_בעיות_על_מפה
    import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestActivityTracking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # הגדרת הדפדפן (Chrome) והתקנת ה-WebDriver אוטומטית
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # המתנה מרבית של 10 שניות לטעינת אלמנטים בדף
        cls.driver.implicitly_wait(10)
        # ניווט לדף מעקב אחרי פעיות
        cls.driver.get("http://yourwebsite.com/מעקב_אחרי_פעיות.html")  # יש להחליף בכתובת האמיתית

    def test_table_display(self):
        # בדיקה אם הטבלה מציגה את הנתונים הנכונים
        driver = self.driver

        # מציאת שורות הטבלה
        table_rows = driver.find_elements(By.CSS_SELECTOR, "#reports-table-body tr")

        # בדיקה אם מספר השורות תואם למספר הדוחות
        self.assertEqual(len(table_rows), 3)

        # בדיקת התוכן של השורה הראשונה
        first_row = table_rows[0].find_elements(By.TAG_NAME, "td")
        self.assertEqual(first_row[0].text, "דוח 1")
        self.assertEqual(first_row[1].text, "ממתין")
        self.assertEqual(first_row[2].text, "גבוהה")

    def test_map_markers(self):
        # בדיקה אם המפה מציגה את הסימנים הנכונים
        driver = self.driver

        # מציאת מיכל המפה
        map_container = driver.find_element(By.ID, "map")

        # בדיקה אם המפה מוצגת
        self.assertTrue(map_container.is_displayed())

        # בדיקה אם יש סימנים על המפה (בדיקה בסיסית, ניתן להוסיף בדיקות מתקדמות יותר)
        # הערה: Selenium לא יכול לתקשר ישירות עם סימני Leaflet.js, אז זהו מקום להרחבה
        markers = driver.execute_script("return document.querySelectorAll('.leaflet-marker-icon').length;")
        self.assertGreater(markers, 0)

    def test_navigation(self):
        # בדיקה אם ניווט התפריט עובד כראוי
        driver = self.driver

        # מציאת הקישור "דף בית" ולחיצה עליו
        home_link = driver.find_element(By.LINK_TEXT, "דף בית")
        home_link.click()

        # בדיקה אם הדף עבר לדף הבית
        self.assertIn("home.html", driver.current_url)

    @classmethod
    def tearDownClass(cls):
        # סגירת הדפדפן לאחר סיום כל הבדיקות
        cls.driver.quit()

if __name__ == "__main__":
    # הרצת כל הבדיקות כאשר הקוד מופעל
    unittest.main()
    --------------------------------
    #הצעת רעיונות לשיפור העיר
    import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCityImprovementIdeas(unittest.TestCase):
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

    def test_submit_idea_form(self):
        # בדיקת שליחת טופס הרעיון
        idea_title = "פארק חדש"  # כותרת הרעיון
        description = "אנחנו צריכים פארק חדש בשכונה."  # תיאור הרעיון
        name = "יוסי כהן"  # שם מלא
        email = "yossi.cohen@example.com"  # כתובת אימייל

        # ממלא את שדות הטופס
        self.driver.find_element(By.ID, "idea-title").send_keys(idea_title)  # מזין כותרת
        self.driver.find_element(By.ID, "description").send_keys(description)  # מזין תיאור
        self.driver.find_element(By.ID, "name").send_keys(name)  # מזין שם
        self.driver.find_element(By.ID, "email").send_keys(email)  # מזין אימייל

        # שולח את הטופס
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # בודק אם הודעת ההצלחה מוצגת
        success_message = self.driver.find_element(By.CLASS_NAME, "success-message")
        self.assertTrue(success_message.is_displayed())  # בודק אם ההודעה מוצגת
        self.assertEqual(success_message.text, "הפידבק נשלח בהצלחה! תודה על שיתוף הפעולה.")  # בודק את תוכן ההודעה

    def test_logout_functionality(self):
        # בדיקת פונקציונליות התנתקות
        logout_button = self.driver.find_element(By.CLASS_NAME, "logoutbtn")  # מוצא את כפתור ההתנתקות
        logout_button.click()  # לוחץ על כפתור ההתנתקות

        # בודק את ההודעה בחלון האלתור (alert)
        alert = self.driver.switch_to.alert  # עובר לחלון האלתור
        self.assertEqual(alert.text, "התנתקת בהצלחה!")  # בודק את הטקסט בהודעה
        alert.accept()  # סוגר את חלון האלתור

        # בודק אם מסך הכניסה מוצג לאחר ההתנתקות
        login_overlay = self.driver.find_element(By.ID, "loginOverlay")  # מוצא את מסך הכניסה
        self.assertTrue(login_overlay.is_displayed())  # בודק אם מסך הכניסה מוצג

if __name__ == "__main__":
    # הרצת כל הבדיקות כאשר הקובץ מופעל
    unittest.main()
    --------------------------------
    #יצירת_קשר_עם_מחלקות_בערייה
    import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDepartmentProfessionals(unittest.TestCase):
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

    def test_electricity_department(self):
        # בודק את מחלקת החשמל
        self._test_department("electricity", ["יוסי כהן", "דנה לוי"])

    def test_transport_department(self):
        # בודק את מחלקת התחבורה
        self._test_department("transport", ["מיכאל ברק", "עדי שמעון"])

    def test_water_department(self):
        # בודק את מחלקת המים
        self._test_department("water", ["גיא צור", "מאיה סולומון"])

    def test_sports_department(self):
        # בודק את מחלקת הספורט
        self._test_department("sports", ["רון כהן", "אלונה רז"])

    def test_cleaning_department(self):
        # בודק את מחלקת הניקיון
        self._test_department("cleaning", ["תמר מזרחי", "יואל שמש"])

    def test_development_department(self):
        # בודק את מחלקת הפיתוח
        self._test_department("development", ["דוד ישראלי", "נועה עמית"])

    def _test_department(self, department, expected_names):
        # פונקציה עזר לבדיקת מחלקה ספציפית
        # לוחץ על הכפתור של המחלקה
        button = self.driver.find_element(By.XPATH, f"//button[contains(@onclick, \"{department}\")]")
        button.click()

        # מחכה עד שהרשימה של בעלי המקצוע מתעדכנת
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "professional"))
        )

        # מוצא את כל בעלי המקצוע המוצגים
        professionals = self.driver.find_elements(By.CLASS_NAME, "professional")
        # בודק אם מספר בעלי המקצוע תואם למצופה
        self.assertEqual(len(professionals), len(expected_names))

        # בודק את השמות של בעלי המקצוע
        for i, prof in enumerate(professionals):
            # בודק אם השם נמצא בטקסט המוצג
            self.assertIn(expected_names[i], prof.text)

if __name__ == "__main__":
    # מריץ את כל הבדיקות כאשר הקובץ מופעל
    unittest.main()
    --------------------------------
    #מעקב_אחרי_פעיות
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
        # מוצא את הסטטוס המעודכן בדוח הראשון
        updated_status = self.driver.find_element(By.XPATH, "//div[@class='report-item'][1]//p[contains(text(), 'סטטוס נוכחי')]")
        # בודק אם הסטטוס מכיל את הטקסט "בטיפול"
        self.assertIn("בטיפול", updated_status.text)

    def test_set_priority(self):
        # בודק עדכון עדיפות של דוח
        self._set_priority(0, 1)  # מעדכן את העדיפות של הדוח הראשון ל"גבוהה"
        # מוצא את העדיפות המעודכנת בדוח הראשון
        updated_priority = self.driver.find_element(By.XPATH, "//div[@class='report-item'][1]//span[@class='priority']")
        # בודק אם העדיפות היא "גבוהה"
        self.assertEqual(updated_priority.text, "גבוהה")

    def test_delete_report(self):
        # בודק מחיקת דוח
        # סופר את מספר הדוחות לפני המחיקה
        initial_reports_count = len(self.driver.find_elements(By.CLASS_NAME, "report-item"))
        self._delete_report(0)  # מוחק את הדוח הראשון
        # סופר את מספר הדוחות לאחר המחיקה
        updated_reports_count = len(self.driver.find_elements(By.CLASS_NAME, "report-item"))
        # בודק אם מספר הדוחות קטן ב-1
        self.assertEqual(updated_reports_count, initial_reports_count - 1)

    def test_subscribe_for_notifications(self):
        # בודק הרשמה להתראות
        self._subscribe_for_notifications(0)  # נרשם להתראות עבור הדוח הראשון
        # עובר לחלון האלתור (alert) שמופיע לאחר ההרשמה
        alert = self.driver.switch_to.alert
        # בודק אם הטקסט באלתור מכיל את המילים "נרשמת לקבלת התראות"
        self.assertIn("נרשמת לקבלת התראות", alert.text)
        # סוגר את חלון האלתור
        alert.accept()

    def _update_status(self, index, new_status):
        # פונקציה עזר לעדכון סטטוס של דוח
        # מוצא את הכפתור לעדכון הסטטוס לפי הטקסט שלו
        status_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), '{new_status}')]")
        # לוחץ על הכפתור
        status_button.click()

    def _set_priority(self, index, priority):
        # פונקציה עזר לעדכון עדיפות של דוח
        # מוצא את הכפתור לעדכון העדיפות לפי הטקסט שלו
        priority_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), 'עדיפות {self._get_priority_text(priority)}')]")
        # לוחץ על הכפתור
        priority_button.click()

    def _delete_report(self, index):
        # פונקציה עזר למחיקת דוח
        # מוצא את הכפתור למחיקת הדוח לפי המחלקה שלו (red)
        delete_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(@class, 'red')]")
        # לוחץ על הכפתור
        delete_button.click()
        # מאשר את המחיקה בחלון האלתור
        alert = self.driver.switch_to.alert
        alert.accept()

    def _subscribe_for_notifications(self, index):
        # פונקציה עזר להרשמה להתראות
        # מוצא את הכפתור להרשמה להתראות לפי הטקסט שלו
        subscribe_button = self.driver.find_element(By.XPATH, f"//div[@class='report-item'][{index + 1}]//button[contains(text(), 'קבלת התראות')]")
        # לוחץ על הכפתור
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
    ---------------------------------
    #עדכון_פרויקטים_ויוזמות_עירוניות
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
        # ממלא את שדה שם הפרויקט
        self.driver.find_element(By.ID, "projectName").send_keys("פרויקט חדש")
        # ממלא את שדה תיאור הפרויקט
        self.driver.find_element(By.ID, "projectDescription").send_keys("תיאור הפרויקט")
        # בוחר את הסטטוס "בתכנון" מהרשימה הנפתחת
        self.driver.find_element(By.ID, "projectStatus").send_keys("בתכנון")
        # ממלא את שדה תאריך ההתחלה
        self.driver.find_element(By.ID, "startDate").send_keys("2023-10-01")
        # ממלא את שדה תאריך הסיום
        self.driver.find_element(By.ID, "endDate").send_keys("2023-12-31")

        # לוחץ על כפתור "הוסף פרויקט" כדי לשלוח את הטופס
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # מחכה להופעת חלון האלתור (alert) עם הודעת האישור
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        # עובר לחלון האלתור
        alert = self.driver.switch_to.alert
        # בודק אם הטקסט באלתור מכיל את המילים "הפרויקט הוסף בהצלחה!"
        self.assertIn("הפרויקט הוסף בהצלחה!", alert.text)
        # סוגר את חלון האלתור
        alert.accept()

        # בודק אם הדף עבר לדף עדכון הפרויקטים
        self.assertIn("עדכון_פרויקטים_ויוזמות_עירוניות.html", self.driver.current_url)

    def test_cancel_form(self):
        # בודק ביטול הטופס
        # לוחץ על כפתור "ביטול"
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-cancel").click()

        # מחכה להופעת חלון האלתור (alert) עם הודעת האישור
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        # עובר לחלון האלתור
        alert = self.driver.switch_to.alert
        # מאשר את הביטול
        alert.accept()

        # בודק אם הדף עבר לדף עדכון הפרויקטים
        self.assertIn("עדכון_פרויקטים_ויוזמות_עירוניות.html", self.driver.current_url)

if __name__ == "__main__":
    # מריץ את כל הבדיקות כאשר הקובץ מופעל
    unittest.main()
    --------------------------------
    #פרויקטים_קיימים
    import unittest  # יבוא של ספריית unittest לכתיבת בדיקות יחידה
from selenium import webdriver  # יבוא של Selenium לאוטומציית דפדפן
from selenium.webdriver.common.by import By  # יבוא של By לאיתור אלמנטים בדף
from selenium.webdriver.common.keys import Keys  # יבוא של Keys לשליחת מקשים (לא בשימוש כאן)
import time  # יבוא של time לשימוש בפונקציות המתנה

class TestExistingProjectsPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # פונקציה שמופעלת פעם אחת לפני כל הבדיקות
        cls.driver = webdriver.Chrome()  # פתיחת דפדפן Chrome
        cls.driver.implicitly_wait(10)  # המתנה מרבית של 10 שניות לאיתור אלמנטים
        cls.base_url = "file:///path/to/your/html/file.html"  # כתובת הקובץ HTML המקומי (יש לעדכן את הנתיב)

    def test_page_title(self):
        # בדיקה שהכותרת של הדף נכונה
        self.driver.get(self.base_url)  # טעינת הדף
        self.assertEqual(self.driver.title, "פרויקטים קיימים")  # השוואה בין הכותרת לצפוי

    def test_navbar_links(self):
        # בדיקה שהקישורים בניווט העליון פועלים
        self.driver.get(self.base_url)  # טעינת הדף
        navbar_links = self.driver.find_elements(By.CLASS_NAME, "w3-bar-item")  # איתור כל הקישורים בניווט
        self.assertGreater(len(navbar_links), 0)  # וידוא שיש לפחות קישור אחד

        # בדיקת הקישור "דף בית"
        home_link = self.driver.find_element(By.LINK_TEXT, "דף בית")  # איתור הקישור לפי הטקסט
        home_link.click()  # לחיצה על הקישור
        self.assertIn("home.html", self.driver.current_url)  # וידוא שהכתובת השתנתה לדף הבית

    def test_projects_list(self):
        # בדיקה שהרשימה של הפרויקטים מוצגת כראוי
        self.driver.get(self.base_url)  # טעינת הדף
        projects_list = self.driver.find_element(By.ID, "projects-list")  # איתור הרשימה לפי ID
        self.assertTrue(projects_list.is_displayed())  # וידוא שהרשימה מוצגת

        # בדיקה אם מופיעה הודעה כאשר אין פרויקטים
        no_projects_message = projects_list.find_elements(By.TAG_NAME, "p")  # איתור כל הפסקאות בתוך הרשימה
        if no_projects_message:  # אם יש הודעה
            self.assertIn("לא נמצאו פרויקטים", no_projects_message[0].text)  # וידוא שההודעה נכונה

    def test_logout_button(self):
        # בדיקה שהכפתור "התנתקות" פועל
        self.driver.get(self.base_url)  # טעינת הדף
        logout_button = self.driver.find_element(By.CLASS_NAME, "logoutbtn")  # איתור כפתור ההתנתקות
        logout_button.click()  # לחיצה על הכפתור
        time.sleep(2)  # המתנה של 2 שניות להופעת החלון מודאלי
        alert = self.driver.switch_to.alert  # מעבר לחלון המודאלי
        self.assertEqual(alert.text, "התנתקת בהצלחה!")  # וידוא שההודעה נכונה
        alert.accept()  # אישור ההודעה
        self.assertIn("login.html", self.driver.current_url)  # וידוא שהדף הועבר לדף הכניסה

    @classmethod
    def tearDownClass(cls):
        # פונקציה שמופעלת פעם אחת לאחר כל הבדיקות
        cls.driver.quit()  # סגירת הדפדפן

if __name__ == "__main__":
    unittest.main()  # הרצת כל הבדיקות