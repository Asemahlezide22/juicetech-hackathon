"""Cellphone verification by one-time PIN.

This mirrors step 2 of the rental flow: "Enter and verify your cellphone
number using OTP". No SMS gateway is wired up yet — while
config.OTP_DEBUG_RETURN_CODE is True the code comes back in the response so
the flow can be demonstrated end to end.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession
from sqlmodel import select

from .. import config, services
from ..config import utcnow
from ..database import get_session
from ..models import OtpCode, Session
from ..schemas import OtpRequestIn, OtpRequestOut, OtpVerifyIn, OtpVerifyOut

router = APIRouter(prefix="/api/otp", tags=["otp"])


def _normalise_phone(raw: str) -> str:
    """Reduce a SA number to digits, dropping a leading 0 or +27.

    "073 407 2268", "0734072268" and "+27 73 407 2268" all become "734072268",
    so a customer is recognised however they type their number.
    """
    digits = "".join(ch for ch in raw if ch.isdigit())

    if digits.startswith("27") and len(digits) > 9:
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = digits[1:]

    if len(digits) != 9:
        raise HTTPException(
            status_code=422,
            detail="Enter a valid South African cellphone number, e.g. 073 407 2268.",
        )
    return digits


@router.post("/request", response_model=OtpRequestOut)
def request_otp(payload: OtpRequestIn, db: DBSession = Depends(get_session)):
    """Issue a fresh OTP for a phone number.

    Any earlier unused codes for that number are invalidated first, so only
    the most recent PIN works.
    """
    phone = _normalise_phone(payload.phone)

    stale = db.exec(
        select(OtpCode).where(OtpCode.phone == phone, OtpCode.consumed == False)  # noqa: E712
    ).all()
    for old in stale:
        old.consumed = True
        db.add(old)

    code = services.make_otp_code()
    entry = OtpCode(
        phone=phone,
        code=code,
        expires_at=utcnow() + timedelta(minutes=config.OTP_TTL_MINUTES),
    )
    db.add(entry)
    db.commit()

    return OtpRequestOut(
        phone=phone,
        expires_in_seconds=config.OTP_TTL_MINUTES * 60,
        message=f"OTP sent to 0{phone}.",
        debug_code=code if config.OTP_DEBUG_RETURN_CODE else None,
    )


@router.post("/verify", response_model=OtpVerifyOut)
def verify_otp(payload: OtpVerifyIn, db: DBSession = Depends(get_session)):
    """Exchange a valid OTP for a session token used to start rentals."""
    phone = _normalise_phone(payload.phone)

    entry = db.exec(
        select(OtpCode)
        .where(OtpCode.phone == phone, OtpCode.consumed == False)  # noqa: E712
        .order_by(OtpCode.created_at.desc())
    ).first()

    if entry is None:
        raise HTTPException(status_code=404, detail="Request an OTP first.")

    if entry.expires_at < utcnow():
        raise HTTPException(status_code=410, detail="That OTP has expired. Request a new one.")

    if entry.attempts >= config.OTP_MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many attempts. Request a new OTP.")

    if entry.code != payload.code:
        entry.attempts += 1
        db.add(entry)
        db.commit()
        remaining = config.OTP_MAX_ATTEMPTS - entry.attempts
        raise HTTPException(
            status_code=401,
            detail=f"Incorrect OTP. {remaining} attempt(s) remaining.",
        )

    entry.consumed = True
    db.add(entry)

    session = Session(
        token=services.make_session_token(),
        phone=phone,
        expires_at=utcnow() + timedelta(hours=config.SESSION_TTL_HOURS),
    )
    db.add(session)
    db.commit()

    return OtpVerifyOut(token=session.token, phone=phone, expires_at=session.expires_at)
