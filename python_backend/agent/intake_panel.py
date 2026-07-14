import asyncio
import json
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from agent.aggregator import Aggregator
from agent.base import RequestContext
from agent.reviewer import SummaryReviewer,CompletenessReviewer,UrgencyReviewer,ConsistencyReviewer
from models.panel_model import Notification,NotificationType,PanelReview,PanelSummary,ReviewStatus
from models.agent_model import AppointmentRequest,RequestStatus
from models.patient_disease_model import Priority
from agent.fetcher import fetch_all_documents

REVIEWERS = [SummaryReviewer(),CompletenessReviewer(),UrgencyReviewer(),ConsistencyReviewer()]

aggregator = Aggregator()

async def run_intake_panel(request_id: str, db: AsyncSession):
    result = await db.execute(
        select(AppointmentRequest).where(AppointmentRequest.id == uuid.UUID(request_id)).options(
            selectinload(AppointmentRequest.documents),
            selectinload(AppointmentRequest.patient)))

    request = result.scalar_one_or_none()
    if not request:
        return
    request.status = RequestStatus.processing
    await db.commit()
    documents = []
    for doc in request.documents:
        documents.append(
            {"url": doc.document_url,"document_type": doc.document_type.value})

    fetched_documents = await fetch_all_documents(documents)
    context = RequestContext(
        request_id=request_id,
        patient_name=f"{request.patient.first_name} {request.patient.last_name}",
        appointment_type=request.appointment_type,
        description=request.description,
        fetched_documents=fetched_documents)

    reviewer_results = await asyncio.gather(*[reviewer.review(context) for reviewer in REVIEWERS],return_exceptions=True)
    cleaned_results = []
    for i, result in enumerate(reviewer_results):
        if isinstance(result, Exception):
            cleaned_results.append(
                {"reviewer": REVIEWERS[i].name,"status": "failed","findings": {},"error": str(result), }
            )
        else:
            cleaned_results.append(result)
    for result in cleaned_results:
        review = PanelReview(
            request_id=uuid.UUID(request_id),
            reviewer_name=result["reviewer"],
            findings=json.dumps(result["findings"]),
            status=(
                ReviewStatus.completed
                if result["status"] == "completed"
                else ReviewStatus.failed),
            error_message=result.get("error"),)
        db.add(review)
    await db.commit()

    final_result = await aggregator.aggregate(cleaned_results)

    summary = PanelSummary(
        request_id=uuid.UUID(request_id),
        summary_text=final_result["summary_text"],
        missing_items=json.dumps(final_result["missing_items"]),
        suggested_priority=Priority(final_result["suggested_priority"]),
        consistency_flags=json.dumps(final_result["consistency_flags"]),
        raw_findings=json.dumps(cleaned_results),)
    db.add(summary)
    request.status = RequestStatus.under_review
    await db.commit()
    await create_notifications(db,request,final_result["suggested_priority"])
    
async def create_notifications(db: AsyncSession,request: AppointmentRequest,priority: str):
    patient_notification = Notification(
        user_id=request.patient_id,
        request_id=request.id,
        type=NotificationType.panel_complete,
        message="Your appointment request has been reviewed and sent to the coordinator.")
    db.add(patient_notification)
    coordinator_notification = Notification(
        user_id=request.patient_id, 
        request_id=request.id,
        type=NotificationType.panel_complete,   
        message=f"New appointment request received. Suggested priority: {priority}.")
    db.add(coordinator_notification)
    await db.commit()