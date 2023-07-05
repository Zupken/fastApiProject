from database import SessionLocal, Base
from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
import re


class Entry(Base):
    __tablename__ = "phone_book"
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    number = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String, index=True)


class EntryCreate(BaseModel):
    first_name: str
    last_name: str
    number: str
    email: EmailStr

    @validator('number')
    def validate_number(cls, number):
        cleaned_number = number.replace(' ', '')
        # E.164 international standard - phone number up to 15 digits
        # min length - +country_code number - so min length is 2 digits
        if not re.match(r'^\+[1-9]{1}[0-9]{1,14}$', cleaned_number):
            if not cleaned_number.startswith('+') and cleaned_number[0].isdigit():
                raise ValueError("No country code.")
            elif len(cleaned_number) < 3:
                raise ValueError('Phone number is too short.')
            else:
                raise ValueError("Invalid number format")
            
        db = SessionLocal()
        entry = db.query(Entry).filter(Entry.number == cleaned_number).first()
        if entry:
            raise ValueError("Number already exists")
        return cleaned_number


class EntryUpdate(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    number: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)

    @validator('number', pre=True, always=True)
    def validate_number(cls, number):
        if number is not None:
            cleaned_number = number.replace(' ', '')
            if not re.match(r'^\+[1-9]{1}[0-9]{1,14}$', cleaned_number):
                if not cleaned_number.startswith('+') and cleaned_number[0].isdigit():
                    raise ValueError("No country code.")
                elif len(cleaned_number) < 3:
                    raise ValueError('Phone number is too short.')
                else:
                    raise ValueError("Invalid number format")
            return cleaned_number


class EntryOut(BaseModel):
    first_name: str
    last_name: str
    number: str
    email: EmailStr

