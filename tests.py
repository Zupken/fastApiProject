import os
os.environ["TESTING"] = "1"

import unittest
from fastapi.testclient import TestClient
from main import app
from models import Entry
from database import SessionLocal, engine, Base



class TestCreatingEntry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_create_entry_valid(self):
        entry_data = {
            "first_name": "John",
            "last_name": "Doe",
            "number": "+12 345 67890",
            "email": "john.doe@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 200)
        entry = Entry(**response.json())
        self.assertEqual(entry.first_name, "John")
        self.assertEqual(entry.last_name, "Doe")
        self.assertEqual(entry.number, "+1234567890")
        self.assertEqual(entry.email, "john.doe@example.com")
    
    def test_create_entry_max_long_number(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "+123456789012345",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 200)
    
    def test_create_entry_min_long_number(self):
        entry_data = {
            "first_name": "John",
            "last_name": "Smith",
            "number": "+12",
            "email": "john.smith@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 200)

    def test_create_entry_no_country_code(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "1234242",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_entry_too_short_number(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "+1",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_entry_too_long_number(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "+1234567890123456",
            "email": "jane.smith@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 422)
    
    def test_create_entry_bad_email(self):
        entry_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "number": "123",
            "email": "jane.smith"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 422)
    

class TestReadingEntry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_reading_all_entries(self):
        response = self.client.get('/entries')
        self.assertEqual(len(response.json()), 3)

    def test_reading_by_email(self):
        response = self.client.get('/entries?email=john.doe@example.com')
        self.assertEqual(response.json()[0]['email'], 'john.doe@example.com')
        self.assertEqual(len(response.json()), 1)

    def test_reading_by_name(self):
        response = self.client.get('/entries?first_name=John&last_name=Doe')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['first_name'], 'John')
        self.assertEqual(response.json()[0]['last_name'], 'Doe')
        self.assertEqual(len(response.json()), 1)
    
    def test_reading_by_number(self):
        response = self.client.get('/entries?number=+1234567890')
        self.assertEqual(response.json()[0]['number'], '+1234567890')
        self.assertEqual(len(response.json()), 1)


class TestDeletingEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        with engine.connect() as connection:
            with connection.begin() as transaction:
                for table in Base.metadata.tables.values():
                    connection.execute(table.delete())

    def test_deleting_entry(self):
        self.client.delete('/entries/+1234567890')
        response = self.client.get('/entries')
        self.assertEqual(len(response.json()), 2)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestCreatingEntry))
    test_suite.addTest(unittest.makeSuite(TestReadingEntry))
    test_suite.addTest(unittest.makeSuite(TestDeletingEntry))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
