from sqlalchemy import Column,ForeignKey,String,Enum,DateTime,func,Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies.session import Base
import uuid
import enum

class DocumentType(str,enum.Enum):
    referral_letter="REFERRAL_LETTER"
    insurance_card="INSURANCE_CARD"
    previous_report="PREVIOUS_REPORT"

class Patient_Doc(Base):
    __tablename__="patient_documents"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    request_id = Column(UUID(as_uuid=True), ForeignKey("appointment_request.id", ondelete="SET NULL"), nullable=True)
    document_url=Column(String,nullable=False)
    document_type=Column(Enum(DocumentType),nullable=False)
    content=Column(Text)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    request=relationship("AppointmentRequest",back_populates="documents")
    request= relationship("AppointmentRequest", back_populates="documents")


