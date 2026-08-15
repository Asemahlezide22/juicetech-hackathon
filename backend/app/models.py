"""Database tables for Juice Tech.

The rental lifecycle is:
    active -> returned          (normal, on time or late)
    active -> overdue           (past due, still out)
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from .config import utcnow


class Station(SQLModel, table=True):
    """A physical charging station."""

    id: str = Field(primary_key=True)  # e.g. "JT-CPT-001"
    venue: str
    online: bool = True
    fast_charge: bool = True
    signal: int = 4  # cellular signal, 0-5
    total_slots: int = 12
    # Decimal degrees (WGS84). Used to find the nearest station to a customer.
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class PowerBank(SQLModel, table=True):
    """A single power bank. Lives in a station slot until it is rented."""

    id: str = Field(primary_key=True)  # e.g. "PB-CPT-0001"
    # None while the bank is out on rental.
    station_id: Optional[str] = Field(default=None, foreign_key="station.id", index=True)
    status: str = Field(default="available", index=True)  # available | rented | maintenance
    charge_percent: int = 100


class Rental(SQLModel, table=True):
    """One rental, from collection to return."""

    reference: str = Field(primary_key=True)  # e.g. "JT-8F3K2A"
    phone: str = Field(index=True)
    package_id: str
    minutes: int
    price: int
    deposit: int
    station_id: str = Field(foreign_key="station.id")
    power_bank_id: str = Field(foreign_key="powerbank.id")
    started_at: datetime = Field(default_factory=utcnow)
    due_at: datetime
    returned_at: Optional[datetime] = None
    return_station_id: Optional[str] = None
    late_fee: int = 0
    status: str = Field(default="active", index=True)  # active | returned | overdue


class OtpCode(SQLModel, table=True):
    """A one-time PIN issued to a phone number."""

    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str = Field(index=True)
    code: str
    expires_at: datetime
    attempts: int = 0
    consumed: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class Session(SQLModel, table=True):
    """Proof that a phone number completed OTP verification."""

    token: str = Field(primary_key=True)
    phone: str = Field(index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=utcnow)


class Enquiry(SQLModel, table=True):
    """An event-hire or general enquiry submitted from the website."""

    id: Optional[int] = Field(default=None, primary_key=True)
    reference: str = Field(index=True)  # e.g. "JT-ENQ-0001"
    name: str
    email: str
    phone: str
    event_type: Optional[str] = None
    event_date: Optional[str] = None
    message: str
    status: str = Field(default="new", index=True)  # new | contacted | quoted | closed
    created_at: datetime = Field(default_factory=utcnow)
