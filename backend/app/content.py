"""Website copy and marketing data.

Ported from the React build's src/lib/jt-data.ts so the HTML pages have a
single source of truth. Business rules (prices, fees) stay in config.py —
this file is only the words around them.
"""

BRAND = {
    "name": "Juice Tech",
    "tagline": "Pay for the time, share the time.",
    "tagline_alt": "Stay Powered. Stay Limitless.",
    "email": "info@juicetech.co.za",
    "phone": "073 407 2268",
    "phone_href": "tel:+27734072268",
    "whatsapp": "062 372 6017",
    "whatsapp_href": "https://wa.me/27623726017",
    "location": "Sea Point, Cape Town, 8005",
}

# Every entry here must have a matching route in routers/pages.py, or the
# navigation will link to a 404.
NAV = [
    {"label": "Home", "url": "/"},
    {"label": "Rent a Power Bank", "url": "/rent-a-power-bank"},
    {"label": "How It Works", "url": "/how-it-works"},
    {"label": "Return", "url": "/return"},
    {"label": "Services", "url": "/services"},
    {"label": "Event Hire", "url": "/event-hire"},
    {"label": "About Us", "url": "/about"},
    {"label": "Contact Us", "url": "/contact"},
]

# Four steps, not eight. Nobody reads eight.
RENT_STEPS = [
    "Scan the QR code on the station",
    "Verify your number by OTP",
    "Pay and collect your power bank",
    "Return it to any station",
]

# The long version, for the How It Works page only.
RENT_STEPS_DETAIL = [
    "Scan the QR code on the Juice Tech station",
    "Enter and verify your cellphone number using OTP",
    "Choose a rental package",
    "Pay securely",
    "Collect the assigned power bank",
    "Charge while moving around",
    "Return the power bank to a Juice Tech station",
    "Receive a return confirmation and receipt",
]

WHY_IT_MATTERS = [
    {"title": "No taxi fare", "body": "No transport, no tickets, no way to pay."},
    {"title": "No help", "body": "A flat phone cannot call anyone."},
    {"title": "No memories", "body": "The photos stop when the battery does."},
]

SERVICES = [
    {
        "title": "Power bank rentals",
        "body": "Scan, pay, go. R150 an hour.",
        "url": "/rent-a-power-bank",
        "cta": "Rent one",
    },
    {
        "title": "Event hire",
        "body": "Stations delivered, set up and monitored. From R3,500.",
        "url": "/event-hire",
        "cta": "See packages",
    },
    {
        "title": "Return anywhere",
        "body": "We find the closest station with a free slot.",
        "url": "/return",
        "cta": "Find a station",
    },
]

EVENT_PACKAGES = [
    {
        "name": "Small Event",
        "price": "R3,500",
        "featured": False,
        "features": [
            "1 station, 12 power banks",
            "Up to 8 hours",
            "Delivery, setup, collection",
        ],
    },
    {
        "name": "Standard Event",
        "price": "R5,500",
        "featured": True,
        "features": [
            "1 station, up to 24 power banks",
            "Up to 12 hours",
            "Delivery, setup, collection",
        ],
    },
    {
        "name": "Large Event",
        "price": "From R15,000",
        "featured": False,
        "features": [
            "Multiple stations, 48+ banks",
            "On-site support",
            "Custom quote",
        ],
    },
]

# Four lines, not ten. Anything else is a conversation, not a price list.
EVENT_EXTRAS = [
    ("Extra station", "R2,500 – R3,500 / day"),
    ("Extra 12 power banks", "R1,500 / day"),
    ("On-site assistant", "R1,800 for 8 hours"),
    ("Outside central Cape Town", "Custom quote"),
]

ABOUT = {
    "intro": "One charged bank serves several people a day, instead of sitting "
             "flat in one person's drawer.",
    "points": [
        {
            "title": "Built for here",
            "body": "Loadshedding and long commutes are normal, not edge cases.",
        },
        {
            "title": "Shared, not sold",
            "body": "Rent by the hour. Don't buy a brick you'll never charge.",
        },
        {
            "title": "Safe by design",
            "body": "Power-only cables. The data pins are physically absent.",
        },
    ],
}

TRUST_POINTS = [
    "OTP cellphone verification",
    "Payment confirmed before release",
    "Refundable R500 deposit",
    "No ID document, ever",
]

# There is no FAQ list any more. Those questions — cost, where to return,
# late fees, phone safety — are what the Ask Juice chat answers, from the
# policy documents in app/policies/, and in five languages rather than one.
# Edit the policy document to change an answer.

