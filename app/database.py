from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import sys

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    print("ERROR: Database environment variables missing")
    sys.exit(1)

# ---------------------------
try:
    root_engine = create_engine(
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/",
        echo=False
    )

    with root_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
        print(f"✔ Database `{DB_NAME}` ready")

except Exception as e:
    print("Failed to create database")
    print(str(e))
    sys.exit(1)

# ---------------------------
try:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        echo=False
    )

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base = declarative_base()

except Exception as e:
    print("Failed to connect to database")
    print(str(e))
    sys.exit(1)

# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()