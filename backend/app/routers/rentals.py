"""Rental lifecycle: collect a power bank, track it, return it.

Late fees are calculated in services.py so the rules stay testable.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession
from sqlmodel import select

from .. import config, services
from ..config import utcnow
from ..database import get_session
from ..deps import current_phone
from ..models import PowerBank, Rental, Station
from ..schemas import RentalOut, RentalReturnIn, RentalStartIn

router = APIRouter(prefix="/api/rentals", tags=["rentals"])


@router.post("", response_model=RentalOut, status_code=201)
def start_rental(
    payload: RentalStartIn,
    phone: str = Depends(current_phone),
    db: DBSession = Depends(get_session),
):
    """Start a rental and release a power bank from the station.

    Requires a verified phone session. One active rental per number.
    """
    package = config.PACKAGES.get(payload.package_id)
    if package is None:
        valid = ", ".join(config.PACKAGES)
        raise HTTPException(status_code=422, detail=f"Unknown package. Choose one of: {valid}.")

    station = db.get(Station, payload.station_id)
    if station is None:
        raise HTTPException(status_code=404, detail=f"Station {payload.station_id} not found.")
    if not station.online:
        raise HTTPException(status_code=409, detail="That station is offline. Try another one.")

    existing = db.exec(
        select(Rental).where(
            Rental.phone == phone,
            Rental.returned_at == None,  # noqa: E711
        )
    ).first()
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail=f"You already have power bank {existing.power_bank_id} out "
                   f"(rental {existing.reference}). Return it before renting again.",
        )

    bank = db.exec(
        select(PowerBank)
        .where(PowerBank.station_id == station.id, PowerBank.status == "available")
        .order_by(PowerBank.charge_percent.desc())  # hand out the fullest bank first
    ).first()
    if bank is None:
        raise HTTPException(
            status_code=409,
            detail="No power banks available at this station right now.",
        )

    started = utcnow()
    rental = Rental(
        reference=services.make_rental_reference(),
        phone=phone,
        package_id=package["id"],
        minutes=package["minutes"],
        price=package["price"],
        deposit=config.DEPOSIT,
        station_id=station.id,
        power_bank_id=bank.id,
        started_at=started,
        due_at=services.due_time(started, package["minutes"]),
    )

    # The bank leaves its slot.
    bank.status = "rented"
    bank.station_id = None

    db.add(rental)
    db.add(bank)
    db.commit()
    db.refresh(rental)

    return services.serialise_rental(rental, utcnow())


@router.get("/{reference}", response_model=RentalOut)
def get_rental(reference: str, db: DBSession = Depends(get_session)):
    """Look up a rental by its reference. Public, so staff can check a code."""
    rental = db.get(Rental, reference.upper())
    if rental is None:
        raise HTTPException(status_code=404, detail=f"No rental found for {reference}.")
    return services.serialise_rental(rental, utcnow())


@router.post("/{reference}/return", response_model=RentalOut)
def return_rental(
    reference: str,
    payload: RentalReturnIn,
    db: DBSession = Depends(get_session),
):
    """Return a power bank to any station and settle the late fee.

    Public because the station itself calls this when a bank clicks into a
    slot — the customer's phone may be flat by then.
    """
    rental = db.get(Rental, reference.upper())
    if rental is None:
        raise HTTPException(status_code=404, detail=f"No rental found for {reference}.")
    if rental.returned_at is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Rental {rental.reference} was already returned.",
        )

    station = db.get(Station, payload.station_id)
    if station is None:
        raise HTTPException(status_code=404, detail=f"Station {payload.station_id} not found.")

    # A station with every slot occupied physically cannot take another bank.
    occupied = len(
        db.exec(select(PowerBank).where(PowerBank.station_id == station.id)).all()
    )
    if occupied >= station.total_slots:
        raise HTTPException(
            status_code=409,
            detail=f"{station.venue} is full. Use /api/stations/nearest?for_return=true "
                   f"to find the closest station with a free slot.",
        )

    now = utcnow()
    rental.late_fee = services.calculate_late_fee(rental, now)
    rental.returned_at = now
    rental.return_station_id = station.id
    rental.status = "returned"

    # The bank takes a slot at whichever station it was returned to.
    bank = db.get(PowerBank, rental.power_bank_id)
    if bank is not None:
        bank.status = "available"
        bank.station_id = station.id
        bank.charge_percent = max(10, bank.charge_percent - 35)  # drained by use
        db.add(bank)

    db.add(rental)
    db.commit()
    db.refresh(rental)

    return services.serialise_rental(rental, now)


@router.get("", response_model=list[RentalOut])
def my_rentals(
    phone: str = Depends(current_phone),
    db: DBSession = Depends(get_session),
):
    """Rental history for the verified phone number, newest first."""
    rentals = db.exec(
        select(Rental).where(Rental.phone == phone).order_by(Rental.started_at.desc())
    ).all()
    now = utcnow()
    return [services.serialise_rental(r, now) for r in rentals]
