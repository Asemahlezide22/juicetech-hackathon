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
    {"label": "AI Operations", "url": "/ai"},
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
            "One station",
            "Up to 8 hours",
            "12 power banks",
            "Delivery within Cape Town",
            "Setup and collection",
            "Remote monitoring",
        ],
    },
    {
        "name": "Standard Event",
        "price": "R5,500",
        "featured": True,
        "features": [
            "One station",
            "Up to 12 hours",
            "12–24 power banks",
            "Digital advertising screen",
            "Setup and collection",
            "Remote monitoring",
        ],
    },
    {
        "name": "Premium Event",
        "price": "R8,500",
        "featured": False,
        "features": [
            "Two stations",
            "Up to 12 hours",
            "Up to 48 power banks",
            "Advertising screens",
            "Setup and collection",
            "One on-site support assistant",
        ],
    },
    {
        "name": "Large Event",
        "price": "From R15,000",
        "featured": False,
        "features": [
            "Multiple stations",
            "48+ power banks",
            "On-site support",
            "Sponsor branding",
            "Event reporting",
            "Custom quote",
        ],
    },
    {
        "name": "Weekend Hire",
        "price": "From R10,500",
        "featured": False,
        "features": [
            "One station Friday–Sunday",
            "Up to 24 power banks",
            "Remote monitoring",
            "Setup and collection",
        ],
    },
]

EVENT_EXTRAS = [
    ("Additional station", "R2,500 – R3,500 / day"),
    ("Additional 12 power banks", "R1,500 / day"),
    ("On-site assistant", "R1,800 for up to 8 hours"),
    ("Additional staff hour", "R250 / hour"),
    ("Custom station branding", "from R1,500"),
    ("Advert displayed on screen", "from R1,000 / event"),
    ("Exclusive screen sponsorship", "R3,500 – R7,500 / event"),
    ("Detailed post-event report", "R750"),
    ("Delivery outside central Cape Town", "Custom quote"),
    ("Overnight or multi-day event", "Custom quote"),
]

ABOUT = {
    "intro": "Juice Tech is a South African shared power bank network. One "
             "charged bank serves several people a day instead of sitting in "
             "one person's drawer.",
    "points": [
        {
            "title": "Built for South Africa",
            "body": "Loadshedding, long commutes and outdoor markets are the "
                    "normal conditions here, not edge cases.",
        },
        {
            "title": "Shared, not sold",
            "body": "Renting by the hour beats buying a power bank that spends "
                    "most of its life flat in a drawer.",
        },
        {
            "title": "Safety first",
            "body": "Power-only cables with the data pins physically absent, so "
                    "a charging station can never read your phone.",
        },
        {
            "title": "POPIA-native",
            "body": "No ID document, no stored card. Personal data is minimised "
                    "at the point of capture.",
        },
    ],
}

TRUST_POINTS = [
    "OTP cellphone verification",
    "Payment confirmed before release",
    "Refundable R500 deposit",
    "Unique customer-to-battery assignment",
    "Automated return reminders",
    "Staff alerts and audit logs",
]

# Four questions. Anything longer and nobody opens any of them.
FAQS = [
    {
        "q": "What does it cost?",
        "a": "R150 an hour, R250 for two. Plus a R500 deposit you get back "
             "on return.",
    },
    {
        "q": "Where do I return it?",
        "a": "Any station with a free slot. The Return page finds the closest one.",
    },
    {
        "q": "What if I'm late?",
        "a": "15 minutes grace, then R75 per half hour. Never more than R750.",
    },
    {
        "q": "Is my phone safe?",
        "a": "Our cables carry power only. The data pins are physically absent, "
             "so nothing can read your phone.",
    },
]

