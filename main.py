from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
import re


DATABASE_URL = "sqlite:///./phone_book.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Entry(Base):
    __tablename__ = "phone_book"

    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    number = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)


class EntryCreate(BaseModel):
    first_name: str
    last_name: str
    number: str
    email: EmailStr

    @validator('number')
    def validate_number(cls, number):
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


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.post("/entry/")
async def create_entry(entry: EntryCreate):
    db = SessionLocal()
    db_entry = Entry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return EntryOut(**db_entry.__dict__)


@app.get("/entries/", response_model=List[EntryOut])
async def read_entries():
    db = SessionLocal()
    entries = db.query(Entry).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found")
    return [EntryOut(**entry.__dict__) for entry in entries]
