from sqlalchemy import Column,ForeignKey,Enum,Text,DateTime,func,Boolean,String
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from dependencies.session import Base
import enum


class ReviewStatus(str,enum.Enum):
    pending="pending"
    completed="completed"

class ReviewerName(str,enum.Enum):
    summarizer="summarizer"

class NotificationType(str,enum.Enum):
    schedule="schedule"
    new_request="new_request"
    otp="otp"
    welcome="welcome"


class PanelReview(Base):
    __tablename__ = "panel_review"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("appointment_request.id", ondelete="CASCADE"), index=True)
    reviewer_name = Column(Enum(ReviewerName), nullable=False)
    findings = Column(Text)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    request = relationship("AppointmentRequest", back_populates="panel_reviews")


class PanelSummary(Base):
    __tablename__ = "panel_summary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("appointment_request.id", ondelete="CASCADE"), unique=True)
    summary_text = Column(Text)
    missing_items = Column(Text)
    suggested_priority = Column(String)
    consistency_flags = Column(Text)
    raw_findings = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    request = relationship("AppointmentRequest", back_populates="panel_summary")


class Notification(Base):
    __tablename__ = "notification"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("appointment_request.id", ondelete="SET NULL"), nullable=True)
    type = Column(Enum(NotificationType))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    request = relationship("AppointmentRequest", back_populates="notifications")