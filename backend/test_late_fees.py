"""Late-fee rules, checked without needing a running server.

Run from the backend/ folder:
    .venv\\Scripts\\python.exe test_late_fees.py

Rule: 15 minutes grace after the due time, then R75 per 30 minutes started,
capped at the R750 replacement fee.
"""

from venv_boot import ensure_venv

ensure_venv()  # must run before the app imports below

from datetime import datetime, timedelta  # noqa: E402

from app.services import calculate_late_fee, minutes_overdue  # noqa: E402
from app.models import Rental  # noqa: E402

START = datetime(2026, 8, 15, 12, 0, 0)

passed = 0
failed = 0


def rental_due_at(minutes: int) -> Rental:
    """A rental that started at noon and ran for `minutes`."""
    return Rental(
        reference="JT-TEST01",
        phone="734072268",
        package_id="1h",
        minutes=minutes,
        price=150,
        deposit=500,
        station_id="JT-CPT-001",
        power_bank_id="PB-001-001",
        started_at=START,
        due_at=START + timedelta(minutes=minutes),
    )


def check(label: str, actual, expected) -> None:
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}: expected {expected}, got {actual}")


print("\nLate fee rules")
print("=" * 60)

r = rental_due_at(60)  # due at 13:00
due = r.due_at

check("returned early - no fee", calculate_late_fee(r, due - timedelta(minutes=20)), 0)
check("returned exactly on time - no fee", calculate_late_fee(r, due), 0)
check("5 min late - inside grace, no fee", calculate_late_fee(r, due + timedelta(minutes=5)), 0)
check("15 min late - grace boundary, no fee", calculate_late_fee(r, due + timedelta(minutes=15)), 0)
check("16 min late - first block, R75", calculate_late_fee(r, due + timedelta(minutes=16)), 75)
check("45 min late - still first block, R75", calculate_late_fee(r, due + timedelta(minutes=45)), 75)
check("46 min late - second block, R150", calculate_late_fee(r, due + timedelta(minutes=46)), 150)
check("75 min late - second block, R150", calculate_late_fee(r, due + timedelta(minutes=75)), 150)
check("76 min late - third block, R225", calculate_late_fee(r, due + timedelta(minutes=76)), 225)

# Cap: 750 / 75 = 10 blocks = 300 chargeable minutes + 15 grace = 315 min
check("5 hours late - capped at R750", calculate_late_fee(r, due + timedelta(hours=5)), 750)
check("3 days late - still capped at R750", calculate_late_fee(r, due + timedelta(days=3)), 750)

# minutes_overdue ignores grace; it is the raw lateness
check("minutes_overdue before due is 0", minutes_overdue(r, due - timedelta(minutes=10)), 0)
check("minutes_overdue counts raw lateness", minutes_overdue(r, due + timedelta(minutes=40)), 40)

# A returned rental is measured to its return time, not to "now"
r_returned = rental_due_at(60)
r_returned.returned_at = due + timedelta(minutes=20)
check(
    "returned rental uses return time, not now",
    calculate_late_fee(r_returned, due + timedelta(days=1)),
    75,
)

print("=" * 60)
print(f"  {passed} passed, {failed} failed\n")
raise SystemExit(1 if failed else 0)
