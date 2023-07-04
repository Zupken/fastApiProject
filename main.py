from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator
import re
import sqlite3



def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("phone_book.db")
        print("Connected to SQLite database")
        return conn
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")
    finally:
        if conn:
            conn.close()


class Item(BaseModel):
    first_name: str
    last_name: str
    number: str
    email: EmailStr

    @validator('number')
    def validate_number(number):
        cleaned_number = number.replace(' ', '')
        #E.164 international standard - phone number up to 15 digits
        #min length - +country_code number - so min length is 3 digits
        if not re.match(r'^\+[1-9]{1}[0-9]{1,14}$', cleaned_number):
            if not cleaned_number.startswith('+') and cleaned_number[0].isdigit():
                raise ValueError("No country code.")   
            elif len(cleaned_number) < 2:
                raise ValueError('Phone number is too short.')
            else:
                raise ValueError("Invalid number format")
        return cleaned_number


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/phone_book")
def get_phone_book():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phone_book")
    rows = cursor.fetchall()
    phone_book = []
    for row in rows:
        entry = {
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "number": row[3],
            "email": row[4]
        }
        phone_book.append(entry)
    return phone_book

@app.post("/item/")
async def create_item(item: Item):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO phone_book (first_name, last_name, number, email) VALUES (?, ?, ?, ?)",
            (item.first_name, item.last_name, item.number, item.email)
        )
    conn.commit()
    return item