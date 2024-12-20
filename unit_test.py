#ahmad zaed#
import unittest
from app import app  # Replace with the actual name of your Flask app file
from io import BytesIO

class TestReportForm(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_missing_description(self):
        response = self.app.post('/submit-report', data={
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (BytesIO(b"test image data"), 'image.png')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid description', response.data)

    def test_long_description(self):
        long_description = 'a' * 501  # Exceeding 500 characters
        response = self.app.post('/submit-report', data={
            'description': long_description,
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (BytesIO(b"test image data"), 'image.png')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid description', response.data)

    def test_missing_coordinates(self):
        response = self.app.post('/submit-report', data={
            'description': 'A valid description',
            'image-upload': (BytesIO(b"test image data"), 'image.png')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Coordinates are missing', response.data)

    def test_invalid_file_type(self):
        response = self.app.post('/submit-report', data={
            'description': 'A valid description',
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (BytesIO(b"test image data"), 'image.txt')  # Invalid file type
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid file type', response.data)

    def test_large_file_size(self):
        large_file = BytesIO(b"x" * (5 * 1024 * 1024 + 1))  # Exceeding 5MB
        response = self.app.post('/submit-report', data={
            'description': 'A valid description',
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (large_file, 'image.png')
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'File size exceeds 5MB', response.data)

    def test_successful_submission(self):
        valid_file = BytesIO(b"test image data")
        response = self.app.post('/submit-report', data={
            'description': 'A valid description',
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (valid_file, 'image.png')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Report submitted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ekram badawia#
import unittest
from app import app, db, Report
from io import BytesIO

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

        # יצירת מסד נתונים חדש לכל בדיקה
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # מחיקת מסד נתונים לאחר כל הבדיקות
        with app.app_context():
            db.drop_all()

    def test_create_report(self):
        """בדיקת יצירת פנייה חדשה"""
        data = {
            'description': 'תיאור המפגע',
            'latitude': '31.0461',
            'longitude': '34.8516',
            'image-upload': (BytesIO(b"image data"), 'test_image.jpg'),
            'date': '20/12/2024'
        }

        response = self.app.post('/report', data=data, follow_redirects=True)

        # לוודא שהסטטוס של הפנייה הוגש כראוי
        self.assertIn(b'סטטוס: הוגשה', response.data)
        self.assertEqual(response.status_code, 200)

    def test_view_reports(self):
        """בדיקת הצגת הפניות בעמוד הבית"""
        # יצירת פנייה לדוגמה
        with app.app_context():
            new_report = Report(
                description='תיאור המפגע',
                latitude=31.0461,
                longitude=34.8516,
                status='הוגשה',
                image_filename='test_image.jpg',
                date='20/12/2024'
            )
            db.session.add(new_report)
            db.session.commit()

        response = self.app.get('/')

        # לוודא שהתיאור של הפנייה נמצא בעמוד הבית
        self.assertIn(b'תיאור המפגע', response.data)
        self.assertIn(b'סטטוס: הוגשה', response.data)
        self.assertIn(b'תאריך הגשה: 20/12/2024', response.data)

    def test_update_report_status(self):
        """בדיקת עדכון סטטוס של פנייה"""
        # יצירת פנייה לדוגמה
        with app.app_context():
            new_report = Report(
                description='תיאור המפגע',
                latitude=31.0461,
                longitude=34.8516,
                status='הוגשה',
                image_filename='test_image.jpg',
                date='20/12/2024'
            )
            db.session.add(new_report)
            db.session.commit()

        response = self.app.post('/status/1', data={'status': 'בטיפול'}, follow_redirects=True)

        # לוודא שהסטטוס עודכן
        self.assertIn(b'סטטוס: בטיפול', response.data)

    def test_view_report_details(self):
        """בדיקת הצגת פרטי פנייה"""
        # יצירת פנייה לדוגמה
        with app.app_context():
            new_report = Report(
                description='תיאור המפגע',
                latitude=31.0461,
                longitude=34.8516,
                status='הוגשה',
                image_filename='test_image.jpg',
                date='20/12/2024'
            )
            db.session.add(new_report)
            db.session.commit()

        response = self.app.get('/status/1')

        # לוודא שהתיאור, הסטטוס, ותאריך ההגשה מוצגים בעמוד הפרטי של הפנייה
        self.assertIn(b'תיאור המפגע', response.data)
        self.assertIn(b'סטטוס: הוגשה', response.data)
        self.assertIn(b'תאריך הגשה: 20/12/2024', response.data)

if _name_ == '_main_':
    unittest.main()
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#sael tori#
import unittest
from app import app, db, Report

class TestGetReports(unittest.TestCase):
    def setUp(self):
        # הגדרת סביבה לבדיקה
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # מסד נתונים בזיכרון
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

        # הוספת דיווחים לדוגמה
        report1 = Report(
            description='פנס רחוב שבור',
            latitude=31.254973,
            longitude=34.792462,
            category='Lighting',
            neighborhood='Downtown',
            image_url='/uploads/lamp_broken.jpg'
        )
        report2 = Report(
            description='פסולת ברחוב',
            latitude=31.250973,
            longitude=34.790462,
            category='Sanitation',
            neighborhood='North',
            image_url='/uploads/trash_street.jpg'
        )
        db.session.add_all([report1, report2])
        db.session.commit()

    def tearDown(self):
        # ניקוי הסביבה לאחר הבדיקה
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_reports_with_filters(self):
        # בדיקה ללא סינון
        response = self.app.get('/get_reports')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

        # בדיקה עם סינון לפי קטגוריה
        response = self.app.get('/get_reports?category=Lighting')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], 'פנס רחוב שבור')

        # בדיקה עם סינון לפי אזור
        response = self.app.get('/get_reports?neighborhood=North')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], 'פסולת ברחוב')

        # בדיקה עם סינון שלא מחזיר תוצאות
        response = self.app.get('/get_reports?category=Infrastructure&neighborhood=South')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)

if _name_ == '_main_':
    unittest.main()
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #tarek abo lel#
    import unittest
from selenium import webdriver

class TestDepartmentLinks(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # יוצר instance של WebDriver - לדוגמה, ChromeDriver
        cls.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # שנה את הנתיב אם צריך
        cls.driver.get('file:///path/to/your/html/file.html')  # קישור לקובץ ה-HTML המקומי שלך

    def test_links(self):
        # בדיקה אם כל כפתור מפנה לדף הנכון
        links = {
            "electricityDept": "פנייה_מחלקת_חשמל.html",
            "transportDept": "פנייה_מחלקת_תחבורה.html",
            "waterDept": "פנייה_מחלקת_מים.html",
            "sportsDept": "פנייה_מחלקת_ספורט.html",
            "cleaningDept": "פנייה_מחלקת_נקיון.html",
            "developmentDept": "פנייה_מחלקת_פתחון.html"
        }
        
        for link_id, expected_href in links.items():
            with self.subTest(link=link_id):
                # חיפוש הכפתור לפי ID
                button = self.driver.find_element_by_id(link_id)
                # השוואה בין ה-HREF של הכפתור לכתובת הצפויה
                self.assertEqual(button.get_attribute("href"), f'file:///path/to/your/html/{expected_href}')

    @classmethod
    def tearDownClass(cls):
        # סוגר את הדפדפן בסיום
        cls.driver.quit()

if _name_ == "_main_":
    unittest.main() 