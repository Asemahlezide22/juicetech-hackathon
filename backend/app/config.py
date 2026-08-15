"""Business rules and pricing for Juice Tech.

These values mirror src/lib/jt-data.ts on the frontend. If a price changes,
change it here and the API will serve the new value to the site automatically.
All money is in South African Rand (ZAR).
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Naive UTC timestamp.

    SQLite does not preserve timezone info, so everything is stored as naive
    UTC. Using this everywhere keeps comparisons safe.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Rental packages offered at every station.
PACKAGES = {
    "1h": {"id": "1h", "label": "1 Hour", "minutes": 60, "price": 150},
    "2h": {"id": "2h", "label": "2 Hours", "minutes": 120, "price": 250},
}

# Refundable security deposit held for the duration of a rental.
DEPOSIT = 500

# Charged when a power bank is never returned.
REPLACEMENT_FEE = 750

# Late returns: free for GRACE_MINUTES, then LATE_FEE_PER_30 per 30 minutes
# (or part thereof). Late fees are capped at REPLACEMENT_FEE.
GRACE_MINUTES = 15
LATE_FEE_PER_30 = 75

# How long an OTP stays valid, and how many times it may be attempted.
OTP_TTL_MINUTES = 5
OTP_MAX_ATTEMPTS = 5

# How long a verified phone session lasts.
SESSION_TTL_HOURS = 12

# Dev convenience: return the OTP in the API response instead of sending an SMS.
# MUST be False in production or anyone can log in as any phone number.
OTP_DEBUG_RETURN_CODE = True

# Origins allowed to call this API (the Vite dev server).
CORS_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
]
