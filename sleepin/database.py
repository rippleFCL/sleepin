import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

environment = os.environ.get("ENV", "prod").lower()


if environment == "dev":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sleepin.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/sleepin.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
