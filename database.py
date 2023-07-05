import os
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
DATABASE_URL = TEST_DATABASE_URL if os.getenv("TESTING") else PRODUCTION_DATABASE_URL
print(DATABASE_URL)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
