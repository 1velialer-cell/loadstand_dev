from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = ("postgresql+psycopg://loadstand:loadstand@localhost/loadstand")

engine = create_engine(
    DATABASE_URL,
    echo=True,)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,)