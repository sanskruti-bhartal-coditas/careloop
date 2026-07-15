from sqlalchemy import Column, String, DateTime,func,Enum
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
import uuid
import enum

class Role(str,enum.Enum):
    patient="PATIENT"
    coordinator="COORDINATOR"
    admin="ADMIN"

class Users(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email=Column(String,unique=True,nullable=False)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    role_name=Column(Enum(Role),nullable=False,default=Role.patient)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
