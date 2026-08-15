"""Event-hire and general enquiries submitted from the website."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession
from sqlmodel import func, select

from ..database import get_session
from ..models import Enquiry
from ..schemas import EnquiryIn, EnquiryOut

router = APIRouter(prefix="/api/enquiries", tags=["enquiries"])


def _next_reference(db: DBSession) -> str:
    """Sequential enquiry reference, e.g. JT-ENQ-0007."""
    count = db.exec(select(func.count()).select_from(Enquiry)).one()
    return f"JT-ENQ-{count + 1:04d}"


@router.post("", response_model=EnquiryOut, status_code=201)
def create_enquiry(payload: EnquiryIn, db: DBSession = Depends(get_session)):
    """Store an enquiry and hand back a reference number."""
    enquiry = Enquiry(
        reference=_next_reference(db),
        name=payload.name.strip(),
        email=payload.email,
        phone=payload.phone.strip(),
        event_type=payload.event_type,
        event_date=payload.event_date,
        message=payload.message.strip(),
    )
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry


@router.get("", response_model=list[EnquiryOut])
def list_enquiries(db: DBSession = Depends(get_session)):
    """All enquiries, newest first — for the staff view."""
    return db.exec(select(Enquiry).order_by(Enquiry.created_at.desc())).all()


@router.get("/{reference}", response_model=EnquiryOut)
def get_enquiry(reference: str, db: DBSession = Depends(get_session)):
    """Look up one enquiry by its reference."""
    enquiry = db.exec(
        select(Enquiry).where(Enquiry.reference == reference.upper())
    ).first()
    if enquiry is None:
        raise HTTPException(status_code=404, detail=f"No enquiry found for {reference}.")
    return enquiry
