"""End-to-end check of the Juice Tech API.

Start the server first, then run this from the backend/ folder:
    .venv\\Scripts\\python.exe smoke_test.py

It walks the full rental journey and prints a pass/fail line for each step.
"""

import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"

passed = 0
failed = 0


def call(method: str, path: str, body: dict | None = None, token: str | None = None):
    """Make a request and return (status_code, parsed_json)."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read() or "null")
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read() or "null")


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}  {detail}")


print("\nJuice Tech API smoke test")
print("=" * 60)

# 1. Health
status, body = call("GET", "/api/health")
check("health endpoint responds", status == 200 and body["status"] == "ok", str(body))

TEST_PHONE = "073 407 2268"


def _authenticate(phone: str) -> str:
    """OTP request + verify, returning a session token."""
    _, otp_body = call("POST", "/api/otp/request", {"phone": phone})
    _, auth_body = call("POST", "/api/otp/verify", {"phone": phone, "code": otp_body["debug_code"]})
    return auth_body["token"]


# --- Cleanup ---------------------------------------------------------------
# Only one rental per number is allowed, so a run that died partway through
# leaves a bank out and blocks every run after it. Clear that first, before
# any station counts are recorded, so the counts below stay accurate.
_setup_token = _authenticate(TEST_PHONE)
_, _my_rentals = call("GET", "/api/rentals", token=_setup_token)

for _old in [r for r in (_my_rentals or []) if r["returned_at"] is None]:
    _, _free = call("GET", "/api/stations/nearest?lat=-33.92&lng=18.42&for_return=true&limit=1")
    if not _free:
        print("  SETUP FAIL  a rental is still out and every station is full.")
        print("              Delete backend/juicetech.db and restart the API to reseed.")
        raise SystemExit(1)
    call("POST", f"/api/rentals/{_old['reference']}/return", {"station_id": _free[0]["id"]})
    print(f"  ....  cleared leftover rental {_old['reference']}")

# 2. Pricing matches the published rates
status, pricing = call("GET", "/api/pricing")
check("pricing returns 200", status == 200)
check("1 hour costs R150", pricing["packages"][0]["price"] == 150, str(pricing))
check("2 hours costs R250", pricing["packages"][1]["price"] == 250)
check("deposit is R300", pricing["deposit"] == 300)
check("late fee is R75 / 30 min", pricing["late_fee_per_30"] == 75)

# 3. Stations
status, stations = call("GET", "/api/stations")
check("station list returns 200", status == 200)
check("4 stations seeded", len(stations) == 4, f"got {len(stations)}")

status, station = call("GET", "/api/stations/JT-CPT-001")
check("homepage station found", status == 200 and station["venue"].startswith("Sea Point"))
banks_before = station["available"]
rented_before = station["rented"]
check("station has stock", banks_before > 0, f"available={banks_before}")

# Pick a station that can actually accept a return, and that is not where we
# collect from. Hard-coding one fills it up after a few runs and every later
# run then fails on a legitimate "station is full" error.
_, all_stations = call("GET", "/api/stations")
_returnable = [
    s for s in all_stations
    if s["id"] != "JT-CPT-001" and s["can_accept_return"] and s["free_slots"] > 1
]
if not _returnable:
    print("  SETUP FAIL  no station has a free slot to return into.")
    print("              Delete backend/juicetech.db and restart the API to reseed.")
    raise SystemExit(1)

RETURN_STATION = max(_returnable, key=lambda s: s["free_slots"])["id"]
return_banks_before = next(
    s["available"] for s in all_stations if s["id"] == RETURN_STATION
)
print(f"  ....  returning to {RETURN_STATION} (most free slots)")

status, missing = call("GET", "/api/stations/JT-NOPE-999")
check("unknown station gives 404", status == 404)

# 3b. Nearest station, measured from Woodstock
status, near = call("GET", "/api/stations/nearest?lat=-33.9276&lng=18.4457&limit=10")
check("nearest returns 200", status == 200, str(near))
check("nearest returns stations", len(near) > 0)
check(
    "sorted closest first",
    all(near[i]["distance_km"] <= near[i + 1]["distance_km"] for i in range(len(near) - 1)),
    str([s["distance_km"] for s in near]),
)
check(
    "Observatory is closest to Woodstock",
    near[0]["id"] == "JT-CPT-004",
    f"got {near[0]['id']} ({near[0]['venue']})",
)
check("distance is plausible", 1 < near[0]["distance_km"] < 5, str(near[0]["distance_km"]))
check("walking time included", near[0]["walking_minutes"] > 0)
check("address included", bool(near[0]["address"]))

status, for_return = call(
    "GET", "/api/stations/nearest?lat=-33.9276&lng=18.4457&for_return=true"
)
check(
    "for_return only lists stations that can accept one",
    all(s["can_accept_return"] and s["free_slots"] > 0 for s in for_return),
    str([(s["id"], s["free_slots"]) for s in for_return]),
)

check("limit is respected", len(call("GET", "/api/stations/nearest?lat=-33.9&lng=18.4&limit=2")[1]) == 2)

status, bad_coords = call("GET", "/api/stations/nearest?lat=999&lng=18.4")
check("out-of-range latitude rejected", status == 422, str(bad_coords))

# 4. Renting without verifying is rejected
status, body = call("POST", "/api/rentals", {"station_id": "JT-CPT-001", "package_id": "1h"})
check("rental without OTP is blocked", status == 401, str(body))

# 5. OTP flow
status, otp = call("POST", "/api/otp/request", {"phone": "073 407 2268"})
check("OTP requested", status == 200 and otp.get("debug_code"), str(otp))
code = otp["debug_code"]

status, bad = call("POST", "/api/otp/verify", {"phone": "0734072268", "code": "000000"})
check("wrong OTP rejected", status == 401, str(bad))

status, auth = call("POST", "/api/otp/verify", {"phone": "+27 73 407 2268", "code": code})
check("correct OTP accepted (any number format)", status == 200 and "token" in auth, str(auth))
token = auth["token"]

# 6. Start a rental
status, rental = call(
    "POST", "/api/rentals", {"station_id": "JT-CPT-001", "package_id": "1h"}, token
)
check("rental started", status == 201, str(rental))
if status != 201:
    # Every check below reads fields off `rental`; without them the cascade of
    # KeyErrors hides the real cause printed above.
    print("=" * 60)
    print(f"  {passed} passed, {failed} failed  (aborted: could not start a rental)\n")
    raise SystemExit(1)

check("price charged is R150", rental["price"] == 150)
check("deposit held is R300", rental["deposit"] == 300)
check("a power bank was assigned", bool(rental["power_bank_id"]))
check("status is active", rental["status"] == "active")
check("about 60 minutes remaining", 58 <= rental["minutes_remaining"] <= 60,
      str(rental["minutes_remaining"]))
reference = rental["reference"]

# 7. Stock dropped by one
status, station = call("GET", "/api/stations/JT-CPT-001")
check("station stock decreased", station["available"] == banks_before - 1,
      f"{station['available']} vs {banks_before - 1}")
check(
    "station rented count went up",
    station["rented"] == rented_before + 1,
    f"{station['rented']} vs {rented_before + 1}",
)

# 8. Second rental on the same number is blocked
status, body = call(
    "POST", "/api/rentals", {"station_id": "JT-CPT-001", "package_id": "2h"}, token
)
check("double rental blocked", status == 409, str(body))

# 9. Look up by reference
status, found = call("GET", f"/api/rentals/{reference}")
check("rental found by reference", status == 200 and found["reference"] == reference)

# 10. Return it (on time, so no late fee)
status, returned = call("POST", f"/api/rentals/{reference}/return", {"station_id": RETURN_STATION})
check("rental returned", status == 200, str(returned))
if status != 200:
    # Everything below reads fields off `returned`; without them the failures
    # are just noise hiding the real cause above.
    print("=" * 60)
    print(f"  {passed} passed, {failed} failed  (aborted after return failed)\n")
    raise SystemExit(1)

check("no late fee on time", returned["late_fee"] == 0)
check("total due is just the R150", returned["total_due"] == 150)
check("status is returned", returned["status"] == "returned")
check("returned to a different station", returned["return_station_id"] == RETURN_STATION)

# 11. Returning twice fails
status, body = call("POST", f"/api/rentals/{reference}/return", {"station_id": RETURN_STATION})
check("double return blocked", status == 409, str(body))

# 12. Bank landed at the return station
status, station2 = call("GET", f"/api/stations/{RETURN_STATION}")
check(
    "bank added to return station",
    station2["available"] == return_banks_before + 1,
    f"{station2['available']} vs {return_banks_before + 1}",
)

# 13. Enquiry
status, enq = call("POST", "/api/enquiries", {
    "name": "Thandi Mokoena",
    "email": "thandi@example.co.za",
    "phone": "0821234567",
    "event_type": "Standard Event",
    "event_date": "2026-09-12",
    "message": "Need a station for a 200-person product launch in Woodstock.",
})
check("enquiry created", status == 201, str(enq))
check("enquiry got a reference", enq.get("reference", "").startswith("JT-ENQ-"), str(enq))

status, body = call("POST", "/api/enquiries", {
    "name": "Bad", "email": "not-an-email", "phone": "0821234567", "message": "hi",
})
check("invalid email rejected", status == 422, str(body))

print("=" * 60)
print(f"  {passed} passed, {failed} failed\n")
raise SystemExit(1 if failed else 0)
