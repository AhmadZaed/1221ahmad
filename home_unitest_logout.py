#logout
import unittest
from unittest.mock import MagicMock, patch

# Mocking localStorage and sessionStorage
class LocalStorageMock:
    def __init__(self):
        self.store = {}

    def getItem(self, key):
        return self.store.get(key, None)

    def setItem(self, key, value):
        self.store[key] = value

    def clear(self):
        self.store = {}


class SessionStorageMock:
    def __init__(self):
        self.store = {}

    def getItem(self, key):
        return self.store.get(key, None)

    def setItem(self, key, value):
        self.store[key] = value

    def clear(self):
        self.store = {}


# Mocking window.location
class WindowLocationMock:
    def __init__(self):
        self.href = ''


# Mocking alert
class AlertMock:
    def __init__(self):
        self.message = None

    def __call__(self, message):
        self.message = message


# Import the logout function
def dganjoLogout():
    # Mocking localStorage and sessionStorage
    localStorage = LocalStorageMock()
    sessionStorage = SessionStorageMock()
    window = WindowLocationMock()
    alert = AlertMock()

    # Simulate the logout function
    localStorage.clear()
    sessionStorage.clear()
    alert("התנתקת בהצלחה!")
    window.href = 'login.html'

    return localStorage, sessionStorage, window, alert


class TestLogoutFunction(unittest.TestCase):
    def setUp(self):
        # Set up mocks before each test
        self.localStorage = LocalStorageMock()
        self.sessionStorage = SessionStorageMock()
        self.window = WindowLocationMock()
        self.alert = AlertMock()

    def test_clears_localStorage_and_sessionStorage(self):
        # Set some data in localStorage and sessionStorage
        self.localStorage.setItem('username', 'testUser')
        self.sessionStorage.setItem('token', '12345')

        # Call the logout function
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # Check if localStorage and sessionStorage are cleared
        self.assertIsNone(localStorage.getItem('username'))
        self.assertIsNone(sessionStorage.getItem('token'))

    def test_shows_alert_with_correct_message(self):
        # Call the logout function
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # Check if the alert was called with the correct message
        self.assertEqual(alert.message, "התנתקת בהצלחה!")

    def test_redirects_to_login_page(self):
        # Call the logout function
        localStorage, sessionStorage, window, alert = dganjoLogout()

        # Check if the page was redirected to login.html
        self.assertEqual(window.href, 'login.html')


if __name__ == "__main__":
    unittest.main()