from sqlalchemy import Column,DateTime,ForeignKey,func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dependencies.session import Base

class Schedule(Base):
    __tablename__="schedule"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    patient_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    assigned_by=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    start_time=Column(DateTime,nullable=False)
    end_time=Column(DateTime,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
