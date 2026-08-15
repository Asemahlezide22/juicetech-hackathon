"""Settings for the JUICE TECH hackathon kiosk demo.

Everything here is simulated. No payment provider is contacted, no card
data is accepted or stored, and no real money moves.
"""

# Shown on every payment screen and in the footer so nobody can mistake
# this for a live system.
DEMO_BADGE = "Hackathon Demo Mode"
DEMO_DISCLAIMER = (
    "This Juice Tech prototype uses simulated transactions. "
    "No real payments are processed."
)

TAGLINE = "Power when you need it."

# The station a QR code points at by default.
DEFAULT_STATION = "JUICE-QR-001"

STATIONS = {
    "JUICE-QR-001": {"id": "JUICE-QR-001", "name": "Juice Mini", "slots": 12},
    "JUICE-QR-002": {"id": "JUICE-QR-002", "name": "Juice Max", "slots": 24},
}

# Rental plans. Prices in South African Rand.
PLANS = {
    "1h": {
        "id": "1h",
        "label": "One hour",
        "minutes": 60,
        "price": 150,
        "blurb": "Enough to get your phone from flat to usable.",
    },
    "2h": {
        "id": "2h",
        "label": "Two hours",
        "minutes": 120,
        "price": 250,
        "blurb": "Stay powered for an event, match or conference.",
    },
}

# Refundable, released when the power bank comes back.
DEPOSIT = 500

PAYMENT_METHODS = [
    {"id": "card", "label": "Card", "hint": "Visa, Mastercard"},
    {"id": "capitec", "label": "Capitec Pay", "hint": "Pay from your Capitec app"},
    {"id": "applepay", "label": "Apple Pay", "hint": "Face ID or Touch ID"},
    {"id": "scan", "label": "Scan to Pay", "hint": "Scan a QR with your phone"},
]

# The ONLY card details the demo will accept. Displayed on screen so nobody
# is ever tempted to type a real one. Nothing here is stored.
TEST_CARD = {
    "number": "4111 1111 1111 1111",
    "expiry": "12/30",
    "cvv": "123",
    "holder": "DEMO CUSTOMER",
}

# Prefilled on the details step so judges can move quickly.
DEMO_CUSTOMER = {
    "name": "Demo Customer",
    "mobile": "071 181 5248",
    "email": "demo@juicetech.co.za",
}

# How long a Scan to Pay QR stays valid.
SCAN_TIMEOUT_MINUTES = 15

# Rental lifecycle.
RENTAL_STATUSES = [
    "started",
    "awaiting_payment",
    "paid_simulated",
    "dispensing",
    "active",
    "returned",
    "cancelled",
    "payment_failed",
]

# Power bank lifecycle.
BANK_STATUSES = [
    "available",
    "reserved",
    "dispensed",
    "rented",
    "returned",
    "charging",
    "offline",
]

# Human-readable labels for the dashboard and receipts.
STATUS_LABELS = {
    "started": "Started",
    "awaiting_payment": "Awaiting payment",
    "paid_simulated": "Paid — simulated",
    "dispensing": "Dispensing",
    "active": "Active",
    "returned": "Returned",
    "cancelled": "Cancelled",
    "payment_failed": "Payment failed",
}


def plan_total(plan_id: str) -> int:
    """Rental fee plus the refundable deposit."""
    return PLANS[plan_id]["price"] + DEPOSIT
