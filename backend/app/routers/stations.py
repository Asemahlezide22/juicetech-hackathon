"""Station endpoints: live availability and finding the nearest station."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session as DBSession
from sqlmodel import select

from .. import services
from ..database import get_session
from ..models import PowerBank, Rental, Station
from ..schemas import NearbyStationOut, StationOut

router = APIRouter(prefix="/api/stations", tags=["stations"])


def _to_out(station: Station, db: DBSession) -> StationOut:
    """Build a station response with live counts.

    "available" is how many charged banks are sitting in this station's slots
    right now. "free_slots" is how many empty slots there are to return a bank
    into — a completely full station cannot accept a return.
    """
    in_slots = db.exec(
        select(PowerBank).where(PowerBank.station_id == station.id)
    ).all()

    available = sum(1 for b in in_slots if b.status == "available")
    free_slots = max(0, station.total_slots - len(in_slots))

    rented = len(
        db.exec(
            select(Rental).where(
                Rental.station_id == station.id,
                Rental.returned_at == None,  # noqa: E711 - SQL NULL check
            )
        ).all()
    )

    return StationOut(
        id=station.id,
        venue=station.venue,
        online=station.online,
        fast_charge=station.fast_charge,
        signal=station.signal,
        total=station.total_slots,
        available=available,
        rented=rented,
        latitude=station.latitude,
        longitude=station.longitude,
        address=station.address,
        free_slots=free_slots,
        can_accept_return=station.online and free_slots > 0,
    )


# NOTE: this must be declared before /{station_id}, otherwise FastAPI matches
# "nearest" as a station id and returns 404.
@router.get("/nearest", response_model=list[NearbyStationOut])
def nearest_stations(
    lat: float = Query(..., ge=-90, le=90, description="Customer latitude"),
    lng: float = Query(..., ge=-180, le=180, description="Customer longitude"),
    limit: int = Query(5, ge=1, le=50),
    for_return: bool = Query(
        False,
        description="Only include stations with a free slot to return a bank into.",
    ),
    db: DBSession = Depends(get_session),
):
    """Stations sorted by how far they are from a coordinate, closest first.

    Pass for_return=true when the customer is returning a power bank — a full
    station is no use to them even if it is the closest one.
    """
    stations = db.exec(select(Station)).all()

    results: list[NearbyStationOut] = []
    for station in stations:
        if station.latitude is None or station.longitude is None:
            continue  # cannot place it on a map

        base = _to_out(station, db)
        if for_return and not base.can_accept_return:
            continue

        km = services.distance_km(lat, lng, station.latitude, station.longitude)
        results.append(
            NearbyStationOut(
                **base.model_dump(),
                distance_km=round(km, 2),
                walking_minutes=services.walking_minutes(km),
            )
        )

    results.sort(key=lambda s: s.distance_km)
    return results[:limit]


@router.get("", response_model=list[StationOut])
def list_stations(db: DBSession = Depends(get_session)):
    """Every station with its current availability."""
    stations = db.exec(select(Station)).all()
    return [_to_out(s, db) for s in stations]


@router.get("/{station_id}", response_model=StationOut)
def get_station(station_id: str, db: DBSession = Depends(get_session)):
    """A single station, for the live card on the homepage."""
    station = db.get(Station, station_id)
    if station is None:
        raise HTTPException(status_code=404, detail=f"Station {station_id} not found.")
    return _to_out(station, db)
