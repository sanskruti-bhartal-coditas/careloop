from sqlalchemy import Column,ForeignKey,String,Enum,Text,DateTime,func,Boolean
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
import enum

class RequestStatus(str,enum.Enum):
    pending="pending"
    submitted="submitted"

class AppointmentRequest(Base):
    __tablename__ = "appointment_request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    appointment_type = Column(String(100))
    description = Column(Text)
    status = Column(Enum(RequestStatus), default=RequestStatus.submitted)
    coordinator_note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    documents = relationship("Patient_Doc", back_populates="request")
    panel_reviews = relationship("PanelReview", back_populates="request", cascade="all, delete-orphan")
    panel_summary = relationship("PanelSummary", back_populates="request", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="request")


