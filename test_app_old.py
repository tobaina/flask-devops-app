import unittest
from app import app

class BasicTests(unittest.TestCase):
    def test_home_status_code(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()