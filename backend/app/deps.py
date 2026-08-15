"""Shared FastAPI dependencies."""

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session as DBSession
from sqlmodel import select

from .config import utcnow
from .database import get_session
from .models import Session


def current_phone(
    authorization: str | None = Header(default=None),
    db: DBSession = Depends(get_session),
) -> str:
    """Resolve the verified phone number from a Bearer session token.

    Raises 401 if the header is missing, malformed, unknown or expired.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify your cellphone number first.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1].strip()
    session = db.exec(select(Session).where(Session.token == token)).first()

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid session. Please verify again.")

    if session.expires_at < utcnow():
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired. Please verify again.")

    return session.phone
