"""HTML pages served by Python.

Plain Jinja2 templates + hand-written CSS + vanilla JavaScript — no build
step, so there is nothing to compile and nothing to download from a CDN.

Every entry in content.NAV must have a route here, or the navigation links
to a 404.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from .. import config, content

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BACKEND_DIR / "templates"))

router = APIRouter(tags=["pages"])

# Fallback for customers who will not or cannot share their GPS location.
# Without this the "find nearest station" feature dead-ends on a denied prompt.
CAPE_TOWN_AREAS = [
    {"name": "Cape Town CBD", "lat": -33.9249, "lng": 18.4241},
    {"name": "Sea Point", "lat": -33.9137, "lng": 18.3866},
    {"name": "Green Point", "lat": -33.9035, "lng": 18.4110},
    {"name": "V&A Waterfront", "lat": -33.9036, "lng": 18.4207},
    {"name": "Observatory", "lat": -33.9376, "lng": 18.4681},
    {"name": "Woodstock", "lat": -33.9276, "lng": 18.4457},
    {"name": "Claremont", "lat": -33.9853, "lng": 18.4649},
    {"name": "Bellville", "lat": -33.9022, "lng": 18.6293},
    {"name": "Khayelitsha", "lat": -34.0403, "lng": 18.6776},
    {"name": "Mitchells Plain", "lat": -34.0353, "lng": 18.6180},
]


def render(request: Request, name: str, **extra):
    """Render a template with the context every page needs."""
    context = {
        "brand": content.BRAND,
        "nav": content.NAV,
        "current_url": request.url.path,
        "packages": list(config.PACKAGES.values()),
        "deposit": config.DEPOSIT,
        "replacement_fee": config.REPLACEMENT_FEE,
        "grace_minutes": config.GRACE_MINUTES,
        "late_fee_per_30": config.LATE_FEE_PER_30,
    }
    context.update(extra)
    return templates.TemplateResponse(request=request, name=name, context=context)


# The station shown on the homepage's live card.
DEMO_STATION_ID = "JT-CPT-001"


@router.get("/", include_in_schema=False)
def home(request: Request):
    return render(
        request,
        "index.html",
        demo_station_id=DEMO_STATION_ID,
        why=content.WHY_IT_MATTERS,
        steps=content.RENT_STEPS,
        services=content.SERVICES,
        trust=content.TRUST_POINTS,
    )


@router.get("/rent-a-power-bank", include_in_schema=False)
def rent(request: Request):
    return render(request, "rent.html", steps=content.RENT_STEPS, trust=content.TRUST_POINTS)


@router.get("/how-it-works", include_in_schema=False)
def how_it_works(request: Request):
    # The only page that earns the full eight-step version.
    return render(request, "how-it-works.html", steps=content.RENT_STEPS_DETAIL)


@router.get("/return", include_in_schema=False)
def return_page(request: Request):
    return render(request, "return.html", areas=CAPE_TOWN_AREAS)


@router.get("/services", include_in_schema=False)
def services(request: Request):
    return render(request, "services.html", services=content.SERVICES)


@router.get("/event-hire", include_in_schema=False)
def event_hire(request: Request):
    return render(
        request,
        "event-hire.html",
        event_packages=content.EVENT_PACKAGES,
        extras=content.EVENT_EXTRAS,
    )


@router.get("/about", include_in_schema=False)
def about(request: Request):
    return render(request, "about.html", about=content.ABOUT, trust=content.TRUST_POINTS)


@router.get("/contact", include_in_schema=False)
def contact(request: Request):
    return render(
        request,
        "contact.html",
        event_packages_names=[p["name"] for p in content.EVENT_PACKAGES],
    )
