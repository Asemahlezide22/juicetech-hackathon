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
    {"label": "Advertising", "url": "/advertising"},
    {"label": "Franchising", "url": "/franchising"},
    {"label": "About Us", "url": "/about"},
    {"label": "Help Centre", "url": "/help-centre"},
    {"label": "Contact Us", "url": "/contact"},
]

RENT_STEPS = [
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
    {
        "title": "Cut off when it matters",
        "body": "No transport, no digital tickets, no mobile payments and no way "
                "to reach the people you came with.",
    },
    {
        "title": "A safety risk",
        "body": "A phone with no charge means no way to call for help, share a "
                "location or contact emergency services.",
    },
    {
        "title": "Moments lost",
        "body": "The photos, videos and memories of the day stop the second the "
                "battery does.",
    },
]

SERVICES = [
    {
        "title": "Power bank rentals",
        "body": "Self-service stations at markets, campuses, malls and taxi ranks. "
                "Scan, verify, pay and go.",
        "url": "/rent-a-power-bank",
        "cta": "Rent a power bank",
    },
    {
        "title": "Event hire",
        "body": "Stations, power banks, delivery, setup, collection and remote "
                "monitoring for your event. From R3,500.",
        "url": "/event-hire",
        "cta": "See event packages",
    },
    {
        "title": "Digital advertising",
        "body": "Large station screens running brand adverts, sponsor messages, "
                "schedules and safety notices.",
        "url": "/advertising",
        "cta": "Advertise with us",
    },
    {
        "title": "Franchising",
        "body": "Equipment, technology, training and sales support to run Juice "
                "Tech in your city.",
        "url": "/franchising",
        "cta": "Explore franchising",
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

ADVERTISING = {
    "intro": "Every Juice Tech station carries a large screen at eye level, in "
             "places where people stop and wait. Advertise where attention "
             "already is.",
    "options": [
        ("Screen advert", "from R1,000 / event", "Your image or video in rotation on station screens."),
        ("Exclusive sponsorship", "R3,500 – R7,500 / event", "Sole brand across every screen at the venue."),
        ("Custom station branding", "from R1,500", "Wrap the station itself in your brand."),
        ("Post-event report", "R750", "Impressions, dwell time and rental volumes."),
    ],
    "process": [
        "Upload your image or video creative",
        "Choose venues, stations and display hours",
        "We approve all content before it goes live",
        "Receive a report after the campaign",
    ],
}

FRANCHISING = {
    "intro": "Juice Tech supplies equipment, technology, training and sales "
             "support to approved franchise partners.",
    "provided": [
        "Charging stations and power bank stock",
        "The rental platform, app and payment integration",
        "Brand assets and marketing templates",
        "Operator training and onboarding",
        "Ongoing technical and sales support",
    ],
    "looking_for": [
        "Local market knowledge and venue relationships",
        "Capacity to service and rebalance stations",
        "A commitment to the Juice Tech service standard",
    ],
}

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

FAQS = [
    {
        "q": "How much does it cost to rent a power bank?",
        "a": "R150 for one hour and R250 for two hours. A refundable R500 security "
             "deposit is held and released once the power bank is returned.",
    },
    {
        "q": "How do I start a rental?",
        "a": "Scan the QR code on any Juice Tech station, verify your cellphone "
             "number with an OTP, choose your package, pay securely and collect "
             "the power bank the station releases for you.",
    },
    {
        "q": "Which cables are included?",
        "a": "Every Juice Tech power bank has built-in Micro-USB, USB-C and "
             "Lightning cables, so you don't need to carry your own.",
    },
    {
        "q": "What happens if I return it late?",
        "a": "A 15-minute grace period applies. After that a late fee of R75 per "
             "additional 30 minutes may be charged, capped at the disclosed "
             "replacement value.",
    },
    {
        "q": "When do I get my deposit back?",
        "a": "The deposit is released as soon as the station confirms the correct "
             "power bank has been returned. Bank processing times may affect when "
             "the refund reflects in your account.",
    },
    {
        "q": "Can I hire Juice Tech for my event?",
        "a": "Yes. Packages start at R3,500 for a single station for up to 8 hours, "
             "including delivery, setup, collection and remote monitoring within "
             "Cape Town.",
    },
    {
        "q": "Where can I return a power bank?",
        "a": "Any Juice Tech station with a free slot — not just the one you "
             "collected from. Use the Return page to find the nearest one.",
    },
]

HELP_ARTICLES = [
    ("How to rent", "Scan the station QR code, verify your number, choose a package, pay and collect the power bank released to you."),
    ("How to return", "Slide the power bank into any empty slot at a Juice Tech station until it clicks. Wait for the on-screen confirmation."),
    ("Payment methods", "Debit and credit cards, Capitec Pay, Instant EFT, Apple Pay, Google Pay and QR payment via Payfast. Staffed events also accept tap to pay and chip and PIN."),
    ("Security deposit and refunds", "A refundable R500 deposit is held for each rental and released on confirmed return. Bank processing can take a few working days."),
    ("Late returns", "A 15-minute grace period applies, then R75 per additional 30 minutes. Late fees never exceed the disclosed replacement value."),
    ("Lost or damaged power banks", "A configurable replacement fee applies (currently R750). Every replacement charge is reviewed by staff first."),
    ("Station did not release a power bank", "Do not pay again. Contact support with your rental reference — failed releases are investigated and refunded or corrected."),
    ("Payment succeeded but no power bank released", "Your rental stays inactive until the station confirms a release, so the charge is reversed or a bank is released manually."),
    ("Event bookings", "Submit the event hire form and you'll receive a reference number plus a quotation. Bookings confirm on a 50% deposit."),
    ("Advertising", "Upload image or video creative, choose venues, stations and display hours. All content is approved before going live."),
    ("Franchising", "Juice Tech supplies equipment, technology, training and sales support to approved franchise partners."),
    ("Privacy", "Personal information is processed according to our privacy policy. Juice Tech never stores raw card details."),
    ("Contacting support", "Email info@juicetech.co.za, call 073 407 2268 or WhatsApp 062 372 6017."),
]
