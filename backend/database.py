import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from dotenv import load_dotenv

#DATABASE_URL = "mysql+pymysql://root:ptk18@db:3306/QuizGeneratorDB"

load_dotenv()

MYSQL_USER = "root"
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = "db"  # Use the service name defined in docker-compose

# Construct the database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"

# Connect to the SQLite database
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# Session Local to handle interactions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata for creating tables
Base = declarative_base()
metadata = MetaData()