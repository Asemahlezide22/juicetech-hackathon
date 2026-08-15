"""Demo state: seeding, references, dispensing, returns, dashboard figures.

Kept out of the router so the flow can be reasoned about (and reset) in one
place. Every amount here is simulated.
"""

from datetime import timedelta

from sqlmodel import Session as DBSession
from sqlmodel import delete, select

from . import demo_config as cfg
from .config import utcnow
from .database import engine
from .demo_models import DemoBank, DemoEvent, DemoRental

# Banks present at seed time, per station. Fewer than the slot count so
# "11 available" looks like a real, partly-used station.
SEED_STOCK = {"JUICE-QR-001": 11, "JUICE-QR-002": 18}


def seed(db: DBSession, force: bool = False) -> None:
    """Create the demo fleet. Does nothing if it already exists."""
    if not force and db.exec(select(DemoBank)).first() is not None:
        return

    if force:
        db.exec(delete(DemoEvent))
        db.exec(delete(DemoRental))
        db.exec(delete(DemoBank))

    for station_id, count in SEED_STOCK.items():
        prefix = "PB" if station_id == cfg.DEFAULT_STATION else "PX"
        for slot in range(1, count + 1):
            db.add(
                DemoBank(
                    id=f"{prefix}-{slot:03d}",
                    station_id=station_id,
                    slot=slot,
                    status="available",
                    # Vary the charge so the dashboard looks alive.
                    battery=100 - (slot % 5) * 7,
                )
            )
    db.commit()


def reset(db: DBSession) -> None:
    """Wipe every demo rental and put all banks back. For the presenter."""
    seed(db, force=True)


def next_reference(db: DBSession) -> str:
    """Sequential, readable reference: JT-2026-0001."""
    count = len(db.exec(select(DemoRental)).all())
    year = utcnow().year
    return f"JT-{year}-{count + 1:04d}"


def station(station_id: str) -> dict:
    """Station details, falling back to the default for an unknown QR."""
    return cfg.STATIONS.get(station_id, cfg.STATIONS[cfg.DEFAULT_STATION])


def available_banks(db: DBSession, station_id: str) -> list[DemoBank]:
    return db.exec(
        select(DemoBank)
        .where(DemoBank.station_id == station_id, DemoBank.status == "available")
        .order_by(DemoBank.slot)
    ).all()


def available_count(db: DBSession, station_id: str) -> int:
    return len(available_banks(db, station_id))


def log(db: DBSession, kind: str, detail: str, reference: str = None, amount: int = 0) -> None:
    db.add(DemoEvent(kind=kind, detail=detail, reference=reference, amount=amount))


def reserve_bank(db: DBSession, rental: DemoRental) -> DemoBank | None:
    """Hold the fullest available bank for this rental."""
    banks = available_banks(db, rental.station_id)
    if not banks:
        return None

    bank = max(banks, key=lambda b: b.battery)
    bank.status = "reserved"
    rental.bank_id = bank.id
    rental.slot = bank.slot
    db.add(bank)
    db.add(rental)
    return bank


def complete_payment(db: DBSession, rental: DemoRental) -> None:
    """Mark the simulated payment as taken and move to dispensing."""
    now = utcnow()
    rental.status = "dispensing"
    rental.paid_at = now
    rental.started_at = now
    rental.due_at = now + timedelta(minutes=rental.minutes or 0)

    bank = db.get(DemoBank, rental.bank_id) if rental.bank_id else None
    if bank is not None:
        bank.status = "dispensed"
        db.add(bank)

    db.add(rental)
    log(db, "payment", f"Simulated payment for {rental.reference}",
        rental.reference, rental.fee + rental.deposit)
    db.commit()


def confirm_dispensed(db: DBSession, rental: DemoRental) -> None:
    """The customer has taken the bank out of the slot."""
    if rental.status != "dispensing":
        return

    rental.status = "active"
    bank = db.get(DemoBank, rental.bank_id) if rental.bank_id else None
    if bank is not None:
        bank.status = "rented"
        db.add(bank)

    db.add(rental)
    log(db, "dispense", f"{rental.bank_id} released from slot {rental.slot}",
        rental.reference)
    db.commit()


def accept_return(db: DBSession, rental: DemoRental) -> None:
    """Bank is back in a slot: complete the rental and refund the deposit."""
    rental.status = "returned"
    rental.returned_at = utcnow()
    rental.refunded = True

    bank = db.get(DemoBank, rental.bank_id) if rental.bank_id else None
    if bank is not None:
        bank.status = "available"
        # Used for a while, so it comes back down a bit.
        bank.battery = max(15, bank.battery - 30)
        db.add(bank)

    db.add(rental)
    log(db, "return", f"{rental.bank_id} returned, R{rental.deposit} deposit refunded",
        rental.reference, rental.deposit)
    db.commit()


def release_bank(db: DBSession, rental: DemoRental) -> None:
    """Put a reserved bank back when a rental is cancelled or fails."""
    bank = db.get(DemoBank, rental.bank_id) if rental.bank_id else None
    if bank is not None and bank.status in {"reserved", "dispensed"}:
        bank.status = "available"
        db.add(bank)


def dashboard(db: DBSession) -> dict:
    """Everything the presenter dashboard shows."""
    banks = db.exec(select(DemoBank)).all()
    rentals = db.exec(select(DemoRental).order_by(DemoRental.created_at.desc())).all()

    paid = [r for r in rentals if r.paid_at is not None]
    returned = [r for r in rentals if r.status == "returned"]
    active = [r for r in rentals if r.status in {"active", "dispensing"}]

    return {
        "banks": banks,
        "available": sum(1 for b in banks if b.status == "available"),
        "rented": sum(1 for b in banks if b.status in {"rented", "dispensed", "reserved"}),
        "returned": len(returned),
        "charging": sum(1 for b in banks if b.status == "charging"),
        "offline": sum(1 for b in banks if b.status == "offline"),
        "revenue": sum(r.fee for r in paid),
        "deposits_held": sum(r.deposit for r in active),
        "deposits_refunded": sum(r.deposit for r in returned),
        "rentals": rentals[:12],
        "events": db.exec(
            select(DemoEvent).order_by(DemoEvent.created_at.desc())
        ).all()[:12],
        "total_rentals": len(rentals),
        "active_rentals": active,
    }
