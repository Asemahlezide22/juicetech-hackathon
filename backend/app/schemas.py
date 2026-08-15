"""Request and response shapes for the API.

These are separate from the database models so we never leak internal columns
(like OTP codes) to the browser.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- Stations -------------------------------------------------------------

class StationOut(BaseModel):
    id: str
    venue: str
    online: bool
    fast_charge: bool
    signal: int
    total: int
    available: int
    rented: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    # Free slots to return a bank into. A full station cannot accept a return.
    free_slots: int = 0
    can_accept_return: bool = True


class NearbyStationOut(StationOut):
    """A station plus how far away it is from the customer."""

    distance_km: float
    walking_minutes: int


# --- OTP ------------------------------------------------------------------

class OtpRequestIn(BaseModel):
    phone: str = Field(min_length=9, max_length=20)


class OtpRequestOut(BaseModel):
    phone: str
    expires_in_seconds: int
    message: str
    # Only populated while OTP_DEBUG_RETURN_CODE is on, so you can demo without SMS.
    debug_code: Optional[str] = None


class OtpVerifyIn(BaseModel):
    phone: str
    code: str = Field(min_length=4, max_length=8)


class OtpVerifyOut(BaseModel):
    token: str
    phone: str
    expires_at: datetime


# --- Rentals --------------------------------------------------------------

class RentalStartIn(BaseModel):
    station_id: str
    package_id: str


class RentalReturnIn(BaseModel):
    station_id: str


class RentalOut(BaseModel):
    reference: str
    phone: str
    package_id: str
    price: int
    deposit: int
    station_id: str
    power_bank_id: str
    started_at: datetime
    due_at: datetime
    returned_at: Optional[datetime]
    return_station_id: Optional[str]
    late_fee: int
    status: str
    minutes_remaining: int
    minutes_overdue: int
    total_due: int


# --- Enquiries ------------------------------------------------------------

class EnquiryIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=9, max_length=20)
    event_type: Optional[str] = None
    event_date: Optional[str] = None
    message: str = Field(min_length=1, max_length=4000)


class EnquiryOut(BaseModel):
    reference: str
    name: str
    email: str
    phone: str
    event_type: Optional[str]
    event_date: Optional[str]
    message: str
    status: str
    created_at: datetime
