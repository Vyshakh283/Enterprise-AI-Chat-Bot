from sqlalchemy import create_engine
from Backend.app.core.configure import settings
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator

# Responsilbilities:
"""1.Create database engine for establishing the connection
   2.Configure the connection pool
   3.Sessioon creation"""

engine=create_engine(
    settings.DATABASE_URL,
    # display generated sql
    echo=settings.DEBUG,
    # checks the connection is existing or not
    pool_pre_ping=True,
    # time duration
    pool_recycle=1800,
    # permanent connection
    pool_size=5,
    
    max_overflow=10
)
# Session creation
session_local=sessionmaker(
    bind=engine,
    # false of clearing the datas
    autocommit=False,
    autoflush=False,
    class_=Session,
    expire_on_commit=False,
    
)

