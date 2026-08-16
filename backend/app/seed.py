"""Seed the database with the demo station network.

Runs on startup. Existing stations are never duplicated, but their
coordinates are backfilled so a database created before the "find nearest
station" feature still works.
"""

from sqlmodel import Session as DBSession
from sqlmodel import select

from .database import engine
from .models import PowerBank, Station

# Real Cape Town coordinates, so "nearest station" gives believable distances.
# JT-CPT-001 is the station shown on the homepage card.
STATIONS = [
    {
        "id": "JT-CPT-001",
        "venue": "Sea Point Promenade Market",
        "address": "Beach Rd, Sea Point, Cape Town, 8005",
        "latitude": -33.9137,
        "longitude": 18.3866,
        "signal": 4,
        "total_slots": 12,
    },
    {
        "id": "JT-CPT-002",
        "venue": "V&A Waterfront Food Court",
        "address": "Dock Rd, V&A Waterfront, Cape Town, 8001",
        "latitude": -33.9036,
        "longitude": 18.4207,
        "signal": 5,
        "total_slots": 12,
    },
    {
        "id": "JT-CPT-003",
        "venue": "Cape Town Stadium Fan Walk",
        "address": "Fritz Sonnenberg Rd, Green Point, Cape Town, 8051",
        "latitude": -33.9035,
        "longitude": 18.4110,
        "signal": 3,
        "total_slots": 24,
    },
    {
        "id": "JT-CPT-004",
        "venue": "Observatory Night Market",
        "address": "Lower Main Rd, Observatory, Cape Town, 7925",
        "latitude": -33.9376,
        "longitude": 18.4681,
        "signal": 4,
        "total_slots": 12,
    },
]

# How many banks are physically in each station at seed time. Fewer than the
# slot count, so "available" looks realistic rather than perfectly full.
STOCK = {"JT-CPT-001": 9, "JT-CPT-002": 11, "JT-CPT-003": 18, "JT-CPT-004": 6}


def seed_if_empty() -> None:
    """Create the station network, or backfill it if it predates coordinates."""
    with DBSession(engine) as db:
        if db.exec(select(Station)).first() is not None:
            _backfill_locations(db)
            return

        for spec in STATIONS:
            db.add(Station(**spec))

            count = STOCK[spec["id"]]
            number = spec["id"].split("-")[-1]  # "001"
            for i in range(1, count + 1):
                db.add(
                    PowerBank(
                        id=f"PB-{number}-{i:03d}",
                        station_id=spec["id"],
                        status="available",
                        # Vary the charge so "fullest bank first" is visible.
                        charge_percent=100 - (i % 4) * 5,
                    )
                )

        db.commit()


def restock() -> dict[str, int]:
    """Put every power bank back where it started.

    A bank returned to a different station stays there, which is correct —
    that is how the real network would work. Over a few dozen test rentals
    it also means one station quietly empties: JT-CPT-001, the one on the
    homepage card, drifted to zero banks while JT-CPT-003 collected them.
    The card then advertises a station with nothing in it.

    Rather than delete and recreate the rows, which would orphan any rental
    pointing at them, this moves the existing banks back and marks them
    available. Returns the resulting count per station.
    """
    with DBSession(engine) as db:
        banks = sorted(db.exec(select(PowerBank)).all(), key=lambda b: b.id)

        i = 0
        for station_id, count in STOCK.items():
            for _ in range(count):
                if i >= len(banks):
                    break
                banks[i].station_id = station_id
                banks[i].status = "available"
                db.add(banks[i])
                i += 1

        # Any bank beyond the seeded totals — added by hand, or left over
        # from an older seed — goes to the largest station rather than
        # being dropped.
        busiest = max(STOCK, key=STOCK.get)
        for bank in banks[i:]:
            bank.station_id = busiest
            bank.status = "available"
            db.add(bank)

        db.commit()

        result: dict[str, int] = {}
        for bank in db.exec(select(PowerBank)).all():
            result[bank.station_id] = result.get(bank.station_id, 0) + 1
        return result


def _backfill_locations(db: DBSession) -> None:
    """Fill in coordinates on stations that were seeded before they existed."""
    changed = False

    for spec in STATIONS:
        station = db.get(Station, spec["id"])
        if station is None or station.latitude is not None:
            continue

        station.latitude = spec["latitude"]
        station.longitude = spec["longitude"]
        station.address = spec["address"]
        db.add(station)
        changed = True

    if changed:
        db.commit()
