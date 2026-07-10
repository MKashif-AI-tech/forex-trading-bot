from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from apps.config import DATABASE_URL


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add it to your .env file.")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker( bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
