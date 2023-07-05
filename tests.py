import unittest
from fastapi.testclient import TestClient
from main import app
from models import Entry

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_create_entry_valid(self):
        entry_data = {
            "first_name": "John",
            "last_name": "Doe",
            "number": "+12 345 67890",
            "email": "john.doe@example.com"
        }
        response = self.client.post("/entry/", json=entry_data)
        self.assertEqual(response.status_code, 200)
        entry = Entry(**response.json())
        self.assertEqual(entry.first_name, "John")
        self.assertEqual(entry.last_name, "Doe")
        self.assertEqual(entry.number, "+1234567890")
        self.assertEqual(entry.email, "john.doe@example.com")

    def test_create_entry_invalid(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "123",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/entry/", json=entry_data)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
