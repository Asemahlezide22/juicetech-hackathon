"""The JUICE TECH kiosk demo.

Scan QR -> choose period -> details -> payment method -> simulated payment
-> station dispenses -> receipt -> return -> simulated deposit refund.

Every payment is simulated. No provider is contacted and no card data is
accepted or stored: the card screen only ever accepts the fixed test number
printed on it, and even that is compared and discarded, never persisted.
"""

import io
from pathlib import Path

import qrcode
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from qrcode.image.svg import SvgPathImage
from sqlmodel import Session as DBSession

from .. import assets
from .. import demo_config as cfg
from .. import demo_service as svc
from ..config import utcnow
from ..database import get_session
from ..demo_models import DemoBank, DemoRental

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BACKEND_DIR / "templates"))

router = APIRouter(tags=["kiosk"])


def render(request: Request, name: str, **extra):
    """Render a kiosk template with the context every screen needs."""
    context = {
        "cfg": cfg,
        "asset_version": assets.version(),
        "badge": cfg.DEMO_BADGE,
        "disclaimer": cfg.DEMO_DISCLAIMER,
        "tagline": cfg.TAGLINE,
        "deposit": cfg.DEPOSIT,
    }
    context.update(extra)
    return templates.TemplateResponse(request=request, name=name, context=context)


def get_rental(db: DBSession, reference: str) -> DemoRental | None:
    return db.get(DemoRental, reference)


def not_found(request: Request, reference: str):
    return render(request, "kiosk/expired.html", reference=reference)


# --------------------------------------------------------------- kiosk home

@router.get("/kiosk", include_in_schema=False)
def kiosk_home(
    request: Request,
    station: str = cfg.DEFAULT_STATION,
    db: DBSession = Depends(get_session),
):
    """What the QR code on the physical station opens."""
    svc.seed(db)
    st = svc.station(station)
    return render(
        request,
        "kiosk/home.html",
        station=st,
        available=svc.available_count(db, st["id"]),
    )


@router.post("/kiosk/start", include_in_schema=False)
def kiosk_start(
    station: str = Form(cfg.DEFAULT_STATION),
    db: DBSession = Depends(get_session),
):
    """Begin a rental and move to the period step."""
    svc.seed(db)
    st = svc.station(station)

    rental = DemoRental(reference=svc.next_reference(db), station_id=st["id"])
    db.add(rental)
    db.commit()

    return RedirectResponse(f"/kiosk/{rental.reference}/period", status_code=303)


# ------------------------------------------------------------ step 1: period

@router.get("/kiosk/{reference}/period", include_in_schema=False)
def period_form(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(
        request,
        "kiosk/period.html",
        rental=rental,
        station=svc.station(rental.station_id),
        plans=list(cfg.PLANS.values()),
    )


@router.post("/kiosk/{reference}/period", include_in_schema=False)
def period_submit(
    request: Request,
    reference: str,
    plan: str = Form(...),
    db: DBSession = Depends(get_session),
):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    chosen = cfg.PLANS.get(plan)
    if chosen is None:
        return RedirectResponse(f"/kiosk/{reference}/period", status_code=303)

    rental.plan_id = chosen["id"]
    rental.minutes = chosen["minutes"]
    rental.fee = chosen["price"]
    rental.deposit = cfg.DEPOSIT
    db.add(rental)
    db.commit()

    return RedirectResponse(f"/kiosk/{reference}/details", status_code=303)


# ----------------------------------------------------------- step 2: details

@router.get("/kiosk/{reference}/details", include_in_schema=False)
def details_form(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(
        request,
        "kiosk/details.html",
        rental=rental,
        plan=cfg.PLANS.get(rental.plan_id),
        demo=cfg.DEMO_CUSTOMER,
        errors={},
    )


@router.post("/kiosk/{reference}/details", include_in_schema=False)
def details_submit(
    request: Request,
    reference: str,
    name: str = Form(""),
    mobile: str = Form(""),
    email: str = Form(""),
    consent: str = Form(""),
    db: DBSession = Depends(get_session),
):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    # Validate and sanitise. No ID number is ever requested.
    name, mobile, email = name.strip()[:80], mobile.strip()[:20], email.strip()[:120]
    digits = "".join(c for c in mobile if c.isdigit())

    errors = {}
    if len(name) < 2:
        errors["name"] = "Enter your first name."
    if len(digits) < 9:
        errors["mobile"] = "Enter a valid mobile number, e.g. 071 181 5248."
    if "@" not in email or "." not in email.split("@")[-1]:
        errors["email"] = "Enter a valid email address."
    if not consent:
        errors["consent"] = "Please accept the demo terms to continue."

    if errors:
        return render(
            request,
            "kiosk/details.html",
            rental=rental,
            plan=cfg.PLANS.get(rental.plan_id),
            demo=cfg.DEMO_CUSTOMER,
            errors=errors,
            values={"name": name, "mobile": mobile, "email": email},
        )

    rental.name, rental.mobile, rental.email = name, mobile, email
    rental.status = "awaiting_payment"
    db.add(rental)
    db.commit()

    return RedirectResponse(f"/kiosk/{reference}/payment", status_code=303)


# ----------------------------------------------------- step 3: payment method

@router.get("/kiosk/{reference}/payment", include_in_schema=False)
def payment_form(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(
        request,
        "kiosk/payment.html",
        rental=rental,
        plan=cfg.PLANS.get(rental.plan_id),
        methods=cfg.PAYMENT_METHODS,
    )


@router.post("/kiosk/{reference}/payment", include_in_schema=False)
def payment_submit(
    request: Request,
    reference: str,
    method: str = Form(...),
    db: DBSession = Depends(get_session),
):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    rental.payment_method = method
    db.add(rental)

    # Hold a bank now so the customer is not charged for stock that is gone.
    if rental.bank_id is None:
        svc.reserve_bank(db, rental)

    db.commit()
    return RedirectResponse(f"/kiosk/{reference}/pay", status_code=303)


# ------------------------------------------------------------- DemoPay screen

@router.get("/kiosk/{reference}/pay", include_in_schema=False)
def pay_screen(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    if rental.bank_id is None:
        return render(request, "kiosk/sold-out.html",
                      rental=rental, station=svc.station(rental.station_id))

    method = next(
        (m for m in cfg.PAYMENT_METHODS if m["id"] == rental.payment_method),
        cfg.PAYMENT_METHODS[0],
    )

    return render(
        request,
        "kiosk/pay.html",
        rental=rental,
        plan=cfg.PLANS.get(rental.plan_id),
        method=method,
        card=cfg.TEST_CARD,
        scan_minutes=cfg.SCAN_TIMEOUT_MINUTES,
        total=rental.fee + rental.deposit,
    )


@router.get("/kiosk/{reference}/qr.svg", include_in_schema=False)
def pay_qr(request: Request, reference: str):
    """QR for Scan to Pay. Points at this same demo, on the phone."""
    url = str(request.base_url).rstrip("/") + f"/kiosk/{reference}/pay"

    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)

    buffer = io.BytesIO()
    qr.make_image(image_factory=SvgPathImage).save(buffer)
    return Response(content=buffer.getvalue(), media_type="image/svg+xml")


@router.post("/kiosk/{reference}/pay/success", include_in_schema=False)
def pay_success(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    svc.complete_payment(db, rental)
    return RedirectResponse(f"/kiosk/{reference}/dispensing", status_code=303)


@router.post("/kiosk/{reference}/pay/fail", include_in_schema=False)
def pay_fail(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    rental.status = "payment_failed"
    svc.release_bank(db, rental)   # do not hold stock for a failed payment
    rental.bank_id = None
    rental.slot = None
    db.add(rental)
    svc.log(db, "payment", f"Simulated payment declined for {reference}", reference)
    db.commit()

    return RedirectResponse(f"/kiosk/{reference}/declined", status_code=303)


@router.post("/kiosk/{reference}/pay/cancel", include_in_schema=False)
def pay_cancel(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    rental.status = "cancelled"
    svc.release_bank(db, rental)
    rental.bank_id = None
    rental.slot = None
    db.add(rental)
    svc.log(db, "payment", f"Rental {reference} cancelled", reference)
    db.commit()

    return RedirectResponse(f"/kiosk?station={rental.station_id}", status_code=303)


@router.get("/kiosk/{reference}/declined", include_in_schema=False)
def declined(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(request, "kiosk/declined.html", rental=rental)


# --------------------------------------------------------------- dispensing

@router.get("/kiosk/{reference}/dispensing", include_in_schema=False)
def dispensing(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(
        request,
        "kiosk/dispensing.html",
        rental=rental,
        station=svc.station(rental.station_id),
        plan=cfg.PLANS.get(rental.plan_id),
    )


@router.post("/kiosk/{reference}/dispensed", include_in_schema=False)
def dispensed(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    svc.confirm_dispensed(db, rental)
    return RedirectResponse(f"/kiosk/{reference}/receipt", status_code=303)


# ------------------------------------------------------------------ receipt

@router.get("/kiosk/{reference}/receipt", include_in_schema=False)
def receipt(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(
        request,
        "kiosk/receipt.html",
        rental=rental,
        station=svc.station(rental.station_id),
        plan=cfg.PLANS.get(rental.plan_id),
        total=rental.fee + rental.deposit,
        status_label=cfg.STATUS_LABELS.get(rental.status, rental.status),
    )


# ------------------------------------------------------------------- return

@router.get("/return-power-bank", include_in_schema=False)
def return_form(request: Request, db: DBSession = Depends(get_session)):
    svc.seed(db)
    return render(request, "kiosk/return.html", error=None, values={})


@router.post("/return-power-bank", include_in_schema=False)
def return_submit(
    request: Request,
    reference: str = Form(""),
    bank_id: str = Form(""),
    db: DBSession = Depends(get_session),
):
    reference, bank_id = reference.strip().upper(), bank_id.strip().upper()
    values = {"reference": reference, "bank_id": bank_id}

    rental = get_rental(db, reference)
    if rental is None:
        return render(request, "kiosk/return.html", values=values,
                      error=f"No rental found for {reference or 'that reference'}.")

    if rental.status == "returned":
        return render(request, "kiosk/return.html", values=values,
                      error=f"{reference} was already returned.")

    if rental.status != "active":
        return render(request, "kiosk/return.html", values=values,
                      error=f"{reference} is not out on rental yet.")

    if bank_id and rental.bank_id and bank_id != rental.bank_id:
        return render(request, "kiosk/return.html", values=values,
                      error=f"{reference} was issued power bank {rental.bank_id}, not {bank_id}.")

    svc.accept_return(db, rental)
    return RedirectResponse(f"/return-power-bank/{reference}/done", status_code=303)


@router.get("/return-power-bank/{reference}/done", include_in_schema=False)
def return_done(request: Request, reference: str, db: DBSession = Depends(get_session)):
    rental = get_rental(db, reference)
    if rental is None:
        return not_found(request, reference)

    return render(request, "kiosk/returned.html", rental=rental,
                  station=svc.station(rental.station_id))


# ---------------------------------------------------------------- dashboard

@router.get("/demo-dashboard", include_in_schema=False)
def dashboard(request: Request, db: DBSession = Depends(get_session)):
    svc.seed(db)
    return render(
        request,
        "kiosk/dashboard.html",
        data=svc.dashboard(db),
        labels=cfg.STATUS_LABELS,
        stations=list(cfg.STATIONS.values()),
    )


@router.post("/demo-dashboard/reset", include_in_schema=False)
def dashboard_reset(db: DBSession = Depends(get_session)):
    svc.reset(db)
    return RedirectResponse("/demo-dashboard", status_code=303)


@router.post("/demo-dashboard/return/{reference}", include_in_schema=False)
def dashboard_return(reference: str, db: DBSession = Depends(get_session)):
    """Presenter shortcut: mark a rental returned without the return screen."""
    rental = get_rental(db, reference)
    if rental is not None and rental.status in {"active", "dispensing"}:
        svc.accept_return(db, rental)
    return RedirectResponse("/demo-dashboard", status_code=303)


@router.post("/demo-dashboard/bank/{bank_id}", include_in_schema=False)
def dashboard_bank(bank_id: str, status: str = Form(...), db: DBSession = Depends(get_session)):
    """Change a bank's availability, to demo an offline or charging unit."""
    bank = db.get(DemoBank, bank_id)
    if bank is not None and status in cfg.BANK_STATUSES:
        bank.status = status
        db.add(bank)
        svc.log(db, "station", f"{bank_id} set to {status}")
        db.commit()
    return RedirectResponse("/demo-dashboard", status_code=303)
