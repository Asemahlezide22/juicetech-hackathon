"""Tables for the kiosk demo.

Kept separate from the main rental tables so the demo can be reset from the
dashboard without touching anything else.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from .config import utcnow


class DemoBank(SQLModel, table=True):
    """A power bank sitting in a demo station slot."""

    id: str = Field(primary_key=True)          # "PB-007"
    station_id: str = Field(index=True)        # "JUICE-QR-001"
    slot: int                                  # 7
    status: str = Field(default="available", index=True)
    battery: int = 100                         # percent


class DemoRental(SQLModel, table=True):
    """One simulated rental, from QR scan to deposit refund."""

    reference: str = Field(primary_key=True)   # "JT-2026-0001"
    station_id: str = Field(index=True)
    status: str = Field(default="started", index=True)

    plan_id: Optional[str] = None
    minutes: Optional[int] = None
    fee: int = 0
    deposit: int = 0

    # Customer details. No ID number, no card data — ever.
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None

    payment_method: Optional[str] = None
    bank_id: Optional[str] = None
    slot: Optional[int] = None

    created_at: datetime = Field(default_factory=utcnow)
    paid_at: Optional[datetime] = None
    started_at: Optional[datetime] = None      # when the bank was released
    due_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    refunded: bool = False


class DemoEvent(SQLModel, table=True):
    """An audit line for the dashboard's recent-activity list."""

    id: Optional[int] = Field(default=None, primary_key=True)
    reference: Optional[str] = Field(default=None, index=True)
    kind: str                                   # "payment", "dispense", "return"
    detail: str
    amount: int = 0
    created_at: datetime = Field(default_factory=utcnow)
