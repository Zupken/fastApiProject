from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import validator

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'phone_book'
    arbitrary_types_allowed = True
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    number = Column(String(20))
    email = Column(String(255))

    @validator('number')
    def validate_number(cls, number):
        cleaned_number = number.replace(' ', '')
        # E.164 international standard - phone number up to 15 digits
        # min length - +country_code number - so min length is 3 digits
        if not re.match(r'^\+[1-9]{1}[0-9]{1,14}$', cleaned_number):
            if not cleaned_number.startswith('+') and cleaned_number[0].isdigit():
                raise ValueError("No country code.")
            elif len(cleaned_number) < 2:
                raise ValueError('Phone number is too short.')
            else:
                raise ValueError("Invalid number format")
        return cleaned_number
