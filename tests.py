import os

os.environ["TESTING"] = "1"

import unittest
from fastapi.testclient import TestClient
from main import app
from models import Entry
from database import SessionLocal, engine, Base



class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Create a new connection to the database.
        print('end of tests')
        with engine.connect() as connection:
            # Begin a new transaction.
            with connection.begin() as transaction:
                # Run a raw SQL query to delete all entries from the table.
                for table in Base.metadata.tables.values():
                    connection.execute(table.delete())



    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

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

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(MyTestCase))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
