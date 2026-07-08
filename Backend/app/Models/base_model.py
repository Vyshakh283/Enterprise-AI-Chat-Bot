from app.database.base import Base
from datetime import datetime
from sqlalchemy import DateTime,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func


class BaseModel(Base):
    # Use abstract base model for not creating the table for this class bacause of this model act as parent for all other classes.
    
    __abstract__ =True
    
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    
    created_at: Mapped[datetime] =mapped_column(DateTime(timezone=True),
                                                server_default=func.now(),
                                                nullable=False)
    updated_at: Mapped[datetime] =mapped_column(DateTime(timezone=True),onupdate=func.now(),
                                                nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False,)