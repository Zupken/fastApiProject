from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator
import re


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


@app.post("/item/")
async def create_item(item: Item):
    return item