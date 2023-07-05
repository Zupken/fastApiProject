from fastapi import FastAPI, HTTPException, Path
from models import Entry, EntryCreate, EntryOut
from database import SessionLocal, DATABASE_URL
from typing import List, Optional
from sqlalchemy import func

app = FastAPI()


@app.get("/entries", response_model=List[EntryOut])
async def search_entries(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    number: Optional[str] = None,
    email: Optional[str] = None,
):
    db = SessionLocal()
    query = db.query(Entry)

    if first_name:
        query = query.filter(func.lower(Entry.first_name) == func.lower(first_name))
    if last_name:
        query = query.filter(func.lower(Entry.last_name) == func.lower(last_name))
    if number:
        #plus sign can be passed only by %2B in url.
        #to make it more user friendly we will add it if its not in request
        if number.startswith('+') is False:
            number = '+'+number.strip()
        query = query.filter(Entry.number == number)
    if email:
        query = query.filter(func.lower(Entry.email) == func.lower(email))
        
    entries = query.all()

    if not entries:
        raise HTTPException(status_code=404, detail="No entries found")
    return [EntryOut(**entry.__dict__) for entry in entries]


@app.post("/entries")
async def create_entry(entry: EntryCreate):
    db = SessionLocal()
    db_entry = Entry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return EntryOut(**db_entry.__dict__)

@app.delete("/entries/{number}")
async def delete_entry(number: str = Path(..., description="The phone number of the entry to delete")):
    db = SessionLocal()
    entry = db.query(Entry).filter(Entry.number == number).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": f"Entry with phone number {number} has been deleted."}

