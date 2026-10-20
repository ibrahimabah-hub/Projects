from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('db_user')}:{os.getenv('db_pass')}@{os.getenv('db_host')}:5432/{os.getenv('db_name')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def _add_tables():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_connection():
    return psycopg2.connect(host = os.getenv('db_host'), database=os.getenv("db_name"), user=os.getenv("db_user"), password=os.getenv("db_pass"))
