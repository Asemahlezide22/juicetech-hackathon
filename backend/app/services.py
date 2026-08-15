"""Core business logic: reference codes, late fees, rental state.

Kept separate from the routers so the rules can be unit-tested without HTTP.
"""

import math
import secrets
import string
from datetime import datetime, timedelta

from . import config
from .models import Rental

# Ambiguous characters (0/O, 1/I) are excluded so references are easy to read
# aloud over the phone and off a station screen.
_REF_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def make_rental_reference() -> str:
    """Short human-readable rental reference, e.g. JT-8F3K2A."""
    body = "".join(secrets.choice(_REF_ALPHABET) for _ in range(6))
    return f"JT-{body}"


def make_otp_code(length: int = 6) -> str:
    """Numeric one-time PIN."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def make_session_token() -> str:
    return secrets.token_urlsafe(32)


def minutes_overdue(rental: Rental, now: datetime) -> int:
    """Whole minutes past the due time, ignoring the grace period.

    Returns 0 when the rental is not yet late.
    """
    end = rental.returned_at or now
    if end <= rental.due_at:
        return 0
    return int((end - rental.due_at).total_seconds() // 60)


def calculate_late_fee(rental: Rental, now: datetime) -> int:
    """Late fee in Rand.

    Free for the first GRACE_MINUTES after the due time. After that,
    LATE_FEE_PER_30 for every 30 minutes started. Never exceeds the
    replacement fee, which is what the customer is told upfront.
    """
    over = minutes_overdue(rental, now)
    if over <= config.GRACE_MINUTES:
        return 0

    chargeable = over - config.GRACE_MINUTES
    blocks = math.ceil(chargeable / 30)
    return min(blocks * config.LATE_FEE_PER_30, config.REPLACEMENT_FEE)


def minutes_remaining(rental: Rental, now: datetime) -> int:
    """Whole minutes left before the rental is due. 0 once due."""
    if rental.returned_at is not None:
        return 0
    remaining = (rental.due_at - now).total_seconds() // 60
    return max(0, int(remaining))


def rental_status(rental: Rental, now: datetime) -> str:
    """Current status, treating a past-due unreturned rental as overdue."""
    if rental.returned_at is not None:
        return "returned"
    if now > rental.due_at:
        return "overdue"
    return "active"


def serialise_rental(rental: Rental, now: datetime) -> dict:
    """Rental plus the live figures the UI needs."""
    status = rental_status(rental, now)
    late_fee = rental.late_fee if rental.returned_at else calculate_late_fee(rental, now)

    return {
        "reference": rental.reference,
        "phone": rental.phone,
        "package_id": rental.package_id,
        "price": rental.price,
        "deposit": rental.deposit,
        "station_id": rental.station_id,
        "power_bank_id": rental.power_bank_id,
        "started_at": rental.started_at,
        "due_at": rental.due_at,
        "returned_at": rental.returned_at,
        "return_station_id": rental.return_station_id,
        "late_fee": late_fee,
        "status": status,
        "minutes_remaining": minutes_remaining(rental, now),
        "minutes_overdue": max(0, minutes_overdue(rental, now) - config.GRACE_MINUTES),
        "total_due": rental.price + late_fee,
    }


def due_time(started_at: datetime, minutes: int) -> datetime:
    return started_at + timedelta(minutes=minutes)


# Mean radius of the Earth in kilometres.
EARTH_RADIUS_KM = 6371.0

# Rough average walking speed in km/h, used to turn a distance into a
# "X min walk" estimate. Deliberately conservative for a busy city pavement.
WALKING_SPEED_KMH = 4.5


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points, in kilometres.

    Haversine formula. Accurate to well within a few metres over city
    distances, which is far more precision than a phone's GPS gives anyway.
    """
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def walking_minutes(km: float) -> int:
    """Rounded walking time for a distance, minimum 1 minute."""
    return max(1, round(km / WALKING_SPEED_KMH * 60))
