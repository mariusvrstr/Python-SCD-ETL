from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import types
from sqlalchemy.dialects.mysql.base import MSBinary
import uuid
# from sqlalchemy import MetaData

## SQL Server
## SQLALCHEMY_DATABASE_URL = "mssql://*localhost*/*test_db*?trusted_connection=yes'"
## SQL Lite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sample_scd.db"
 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()

def get_db_Session() -> Session:
    db = session_local()
    return db

