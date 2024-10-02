from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

DATABASE_URL = "sqlite:///./data.db"  # SQLite URL for local database

# Connect to the SQLite database
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session Local to handle interactions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata for creating tables
Base = declarative_base()
metadata = MetaData()