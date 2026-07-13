from sqlalchemy import String,Column,ForeignKey,Float,Integer
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
import uuid

class Patient(Base):
    __tablename__="patient_details"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    weight=Column(Float,nullable=False)
    height=Column(Float,nullable=False)
    age=Column(Integer,nullable=False)
    blood_group=Column(String,nullable=False)
