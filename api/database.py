import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

#database Url
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#engine Created
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#creating session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for models
Base = declarative_base()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

