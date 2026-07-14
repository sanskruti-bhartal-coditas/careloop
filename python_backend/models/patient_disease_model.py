from sqlalchemy import Column,ForeignKey,String,Text,Enum,DateTime,func
from dependencies.session import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
import enum

class Priority(str,enum.Enum):
    routine="routine"
    soon="soon"
    urgent="urgent"

class Patient_Disease(Base):
    __tablename__="patient_disease"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    patient_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    disease=Column(String,nullable=False)
    description=Column(Text)    
    priority=Column(Enum(Priority),nullable=False,default=Priority.routine)
    created_at=Column(DateTime(timezone=True),server_default=func.now())


