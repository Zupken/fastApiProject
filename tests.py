import unittest
from fastapi.testclient import TestClient
from main import app, Item

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_create_item_valid(self):
        item_data = {
            "first_name": "John",
            "last_name": "Doe",
            "number": "+12 345 67890",
            "email": "john.doe@example.com"
        }
        response = self.client.post("/item/", json=item_data)
        self.assertEqual(response.status_code, 200)
        item = Item(**response.json())
        self.assertEqual(item.first_name, "John")
        self.assertEqual(item.last_name, "Doe")
        self.assertEqual(item.number, "+1234567890")
        self.assertEqual(item.email, "john.doe@example.com")

    def test_create_item_invalid(self):
        item_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "123",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/item/", json=item_data)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
