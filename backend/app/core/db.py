from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base ,sessionmaker
from pathlib import Path
import os
from dotenv import load_dotenv

# BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL FOUND:", DATABASE_URL is not None)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    FastAPI Dependency
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



