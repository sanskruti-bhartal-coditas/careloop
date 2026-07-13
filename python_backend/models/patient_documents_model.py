from sqlalchemy import Column,ForeignKey,String,Enum,DateTime,func
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
import uuid
import enum

class DocumentType(str,enum.Enum):
    referral_letter="referral_letter"
    insurance_card="insurance_card"
    previous_report="previous_report"

class Patient_Doc(Base):
    __tablename__="patient_documents"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    document_url=Column(String,nullable=False)
    document_type=Column(Enum(DocumentType),nullable=False)
    chunks=Column(Vector(384))
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    




