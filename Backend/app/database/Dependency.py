from Backend.app.core.configure import settings
from Backend.app.database.db import engine
from Backend.app.database.db import session_local
from collections.abc import Generator
from sqlalchemy.orm import Session,sessionmaker

# Dependency injection
def get_db()->Generator[Session,None,None]:
    
    # Creation of session
    db_ins=session_local()
    try:
        yield db_ins
        
    finally:
        db_ins.close()
        
