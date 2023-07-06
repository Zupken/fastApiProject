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
    
    def test_create_entry_valid2(self):
        entry_data = {
            "first_name": "Adam",
            "last_name": "Cruze",
            "number": "+12345",
            "email": "adam.cruze@example.com"
        }
        response = self.client.post("/entries", json=entry_data)
        self.assertEqual(response.status_code, 200)
        entry = Entry(**response.json())
        self.assertEqual(entry.first_name, "Adam")
        self.assertEqual(entry.last_name, "Cruze")
        self.assertEqual(entry.number, "+12345")
        self.assertEqual(entry.email, "adam.cruze@example.com")
    
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
        self.assertEqual(len(response.json()), 4)

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
        response = self.client.get('/entries?number=%2B1234567890')
        self.assertEqual(response.json()[0]['number'], '+1234567890')
        self.assertEqual(len(response.json()), 1)


class TestUpdatingEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    def test_updating_entry_without_changing_number(self):
        data = {        
            "first_name": "John",
            "last_name": "Does",
            "number": "+7777",
            "email": "johndoe@example.com"
        }
        response = self.client.put('/entries/+12', json=data)
        self.assertEqual(response.status_code, 200)

    def test_updating_entry_with_legal_changing_number_no_email(self):
        data = {        
            "first_name": "John",
            "last_name": "dsaDoes",
            "number": "+999999"
        }
        response = self.client.put('/entries/+1234567890', json=data)
        self.assertEqual(response.status_code, 200)
    
    def test_updating_entry_with_illegal_changing_number(self):
        #we are trying to change number +12345 to number that exists in database
        #that operation is not allowed - we should get 422 code
        data = {        
            "first_name": "John",
            "last_name": "dsaDoes",
            "number": "+123456789012345",
            "email": "johndoe@example.com"
        }
        response = self.client.put('/entries/+12345', json=data)
        self.assertEqual(response.status_code, 422)


class TestDeletingEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    @classmethod
    def tearDownClass(cls):
        #delete all records in database after all tests in that class
        with engine.connect() as connection:
            with connection.begin() as transaction:
                for table in Base.metadata.tables.values():
                    connection.execute(table.delete())

    def test_deleting_entry(self):
        response = self.client.get('/entries')
        number_of_entries = len(response.json())
        self.client.delete('/entries/+999999')
        response = self.client.get('/entries')
        self.assertEqual(len(response.json()), number_of_entries-1)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestCreatingEntry))
    test_suite.addTest(unittest.makeSuite(TestReadingEntry))
    test_suite.addTest(unittest.makeSuite(TestUpdatingEntry))
    test_suite.addTest(unittest.makeSuite(TestDeletingEntry))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
