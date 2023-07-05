# main.py

from fastapi import FastAPI, HTTPException, Path
from models import Entry, EntryCreate, EntryOut
from database import SessionLocal
from typing import List

app = FastAPI()


def get_test_db():
    test_db = SessionLocal()
    return test_db


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

@app.get("/entries/firstname/{firstname}", response_model=List[EntryOut])
async def read_entries_by_firstname(firstname: str):
    db = SessionLocal()
    entries = db.query(Entry).filter(Entry.first_name == firstname).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found")
    return [EntryOut(**entry.__dict__) for entry in entries]


@app.delete("/entry/{number}")
async def delete_entry(number: str = Path(..., description="The phone number of the entry to delete")):
    db = SessionLocal()
    entry = db.query(Entry).filter(Entry.number == number).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": f"Entry with phone number {number} has been deleted."}
