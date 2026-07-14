import json
import uuid
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.agent_model import AppointmentRequest,RequestStatus
from models.panel_model import PanelSummary
from models.patient_documents_model import Patient_Doc
from dependencies.session import get_db
from agent.intake_panel import run_intake_panel
from dependencies.logger import logger
from models.panel_model import Notification, NotificationType


router = APIRouter(prefix="/agent", tags=["Appointment Requests"])


class CreateRequestBody(BaseModel):
    patient_id: uuid.UUID
    appointment_type: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    document_ids: list[uuid.UUID] = []


class UpdateStatusBody(BaseModel):
    new_status: RequestStatus
    coordinator_note: Optional[str] = None


class PanelSummaryOut(BaseModel):
    summary_text: str
    missing_items: list[str]
    suggested_priority: str
    consistency_flags: list[str]

    @classmethod
    def from_orm(cls, row: PanelSummary):
        return cls(
            summary_text=row.summary_text,
            missing_items=json.loads(row.missing_items),
            suggested_priority=row.suggested_priority.value,
            consistency_flags=json.loads(row.consistency_flags),
        )


class RequestOut(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    appointment_type: str
    description: str
    status: str
    coordinator_note: Optional[str]
    panel_summary: Optional[PanelSummaryOut]

    class Config:
        from_attributes = True


@router.post("")
async def create_request(body: CreateRequestBody,background_tasks: BackgroundTasks,db: AsyncSession = Depends(get_db),
):
    try:
        request = AppointmentRequest(
            patient_id=body.patient_id,
            appointment_type=body.appointment_type,
            description=body.description,
            status=RequestStatus.submitted)


        db.add(request)
        await db.flush()

        for doc_id in body.document_ids:
            result = await db.execute(select(Patient_Doc).where(Patient_Doc.id == doc_id))
            document = result.scalar_one_or_none()
            if not document:
                await db.rollback()
                raise HTTPException(
                    status_code=404,
                    detail=f"Document {doc_id} not found")

            if document.user_id != body.patient_id:
                await db.rollback()
                raise HTTPException(status_code=403,detail="Document does not belong to this patient")
            document.request_id = request.id

        await db.commit()

        background_tasks.add_task(run_panel,str(request.id))

        return {
            "message": "Request submitted successfully.",
            "request_id": str(request.id),
            "status": request.status.value,
        }
    except Exception as e:
        raise e

async def run_panel(request_id: str):
    async with get_db() as db:
        try:
            await run_intake_panel(
                request_id=request_id,
                db=db)
        except Exception as e:
            logger.error(e)

            result = await db.execute(select(AppointmentRequest).where(
AppointmentRequest.id == uuid.UUID(request_id)))

            request = result.scalar_one_or_none()

            if request:
                request.status = RequestStatus.submitted
                await db.commit()

@router.get("")
async def list_requests(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(AppointmentRequest)
            .options(selectinload(AppointmentRequest.panel_summary),selectinload(AppointmentRequest.patient))
            .order_by(AppointmentRequest.created_at.desc()))

        requests = result.scalars().all()

        priority_order = {
            "urgent": 0,
            "soon": 1,
            "routine": 2,
            None: 3,
        }

        requests = sorted(
            requests,
            key=lambda r: priority_order.get(
                r.panel_summary.suggested_priority.value
                if r.panel_summary
                else None,
                3,),)

        return [_serialize_request(request) for request in requests]
    except Exception as e:
        raise e


@router.get("/{request_id}")
async def get_request(request_id: uuid.UUID,db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AppointmentRequest)
        .where(AppointmentRequest.id == request_id)
        .options(
            selectinload(AppointmentRequest.panel_summary),
            selectinload(AppointmentRequest.panel_reviews),
            selectinload(AppointmentRequest.documents),
            selectinload(AppointmentRequest.patient),
        )
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404,detail="Request not found",)

    response = _serialize_request(request)

    response["reviewer_details"] = [
        {
            "reviewer": review.reviewer_name.value,
            "status": review.status.value,
            "findings": json.loads(review.findings),
        }
        for review in request.panel_reviews
    ]

    return response

@router.post("/{request_id}/reprocess")
async def reprocess_request(
    request_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AppointmentRequest)
        .where(AppointmentRequest.id == request_id)
        .options(
            selectinload(AppointmentRequest.panel_summary),
            selectinload(AppointmentRequest.panel_reviews)))

    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404,detail="Request not found",)

    for review in request.panel_reviews:
        await db.delete(review)

    if request.panel_summary:
        await db.delete(request.panel_summary)

    request.status = RequestStatus.submitted

    await db.commit()

    background_tasks.add_task(run_panel,str(request.id))

    return {
        "message": "Reprocessing started",
        "request_id": str(request.id)}
    
@router.patch("/{request_id}/status")
async def update_request_status(request_id: uuid.UUID,body: UpdateStatusBody,db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AppointmentRequest).where(AppointmentRequest.id == request_id))
    
    request = result.scalar_one_or_none()

    if not request:
        raise HTTPException(status_code=404,detail="Request not found",) 

    if request.status not in [RequestStatus.under_review,RequestStatus.info_needed]:
        raise HTTPException(status_code=400,detail="Invalid request status")

    if (body.new_status in [RequestStatus.info_needed,RequestStatus.declined]and not body.coordinator_note):
        raise HTTPException(status_code=400,detail="Coordinator note is required",)
    request.status = body.new_status
    request.coordinator_note = body.coordinator_note

    await db.commit()

    await notify_patient(db,request,body.new_status,body.coordinator_note,)

    return {
        "message": "Status updated successfully",
        "request_id": str(request.id),
        "status": request.status.value,}

def _serialize_request(request: AppointmentRequest):
    return {
        "id": str(request.id),
        "patient_id": str(request.patient_id),
        "patient_name": (
            f"{request.patient.first_name} {request.patient.last_name}"
            if request.patient
            else None),
        "appointment_type": request.appointment_type,
        "description": request.description,
        "status": request.status.value,
        "coordinator_note": request.coordinator_note,
        "panel_summary": (
            PanelSummaryOut.from_orm(request.panel_summary).dict()
            if request.panel_summary
            else None),
        "created_at": (request.created_at.isoformat() if request.created_at else None)}


async def notify_patient(db: AsyncSession,request: AppointmentRequest,status: RequestStatus,note: Optional[str]):
   
    if status == RequestStatus.scheduled:
        message = "Your appointment has been scheduled."
        notification_type = NotificationType.request_scheduled

    elif status == RequestStatus.info_needed:
        message = f"Coordinator requested more information. {note}"
        notification_type = NotificationType.info_requested

    elif status == RequestStatus.declined:
        message = f"Your request was declined. {note}"
        notification_type = NotificationType.request_declined

    else:
        message = f"Status changed to {status.value}"
        notification_type = NotificationType.panel_complete

    notification = Notification(
        user_id=request.patient_id,
        request_id=request.id,
        type=notification_type,
        message=message)

    db.add(notification)
    await db.commit()