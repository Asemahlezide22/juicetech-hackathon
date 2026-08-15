"""End-to-end check of the JUICE TECH kiosk demo.

Start the server, then run from the backend/ folder:
    python test_kiosk.py

Walks the exact journey the judges will: scan -> period -> details ->
payment method -> simulated payment -> dispense -> receipt -> return ->
simulated refund. Also checks the failure and cancellation paths, and that
no screen ever loses its demo labelling.
"""

from venv_boot import ensure_venv

ensure_venv()

import re  # noqa: E402
import urllib.error  # noqa: E402
import urllib.parse  # noqa: E402
import urllib.request  # noqa: E402

BASE = "http://127.0.0.1:8000"

passed = 0
failed = 0


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep 303s visible so we can assert on where the flow sends people."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = urllib.request.build_opener(NoRedirect)


def squash(html: str) -> str:
    """Collapse runs of whitespace to single spaces.

    Templates wrap sentences across lines for readability, which would
    otherwise break a plain "phrase in body" check for no good reason.
    """
    return re.sub(r"\s+", " ", html)


def get(path: str):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, squash(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, squash(e.read().decode("utf-8", "replace"))


def post(path: str, data: dict):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(BASE + path, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with opener.open(req) as r:
            return r.status, r.headers.get("Location", ""), squash(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", ""), squash(e.read().decode("utf-8", "replace"))


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}  {detail}")


print("\nJUICE TECH kiosk demo")
print("=" * 62)

# Start from a known state so counts are predictable.
post("/demo-dashboard/reset", {})

# --- 1. The QR code lands somewhere useful ---------------------------------
status, home = get("/kiosk?station=JUICE-QR-001")
check("kiosk page loads", status == 200)
check("shows the station name", "Juice Mini" in home)
check("shows the station id", "JUICE-QR-001" in home)
check("shows availability", "11" in home)
check("has a Start Rental button", "Start Rental" in home)
check("demo badge present", "Hackathon Demo Mode" in home)
check("disclaimer present", "No real payments are processed" in home)

# An unknown QR should still work rather than 404 in front of a judge.
status, unknown = get("/kiosk?station=NOT-A-STATION")
check("unknown station falls back", status == 200 and "Juice Mini" in unknown)

# --- 2. Start a rental -----------------------------------------------------
status, location, _ = post("/kiosk/start", {"station": "JUICE-QR-001"})
check("start redirects to period", status == 303 and location.endswith("/period"), location)
ref = location.split("/kiosk/")[1].split("/")[0]
check("reference looks right", re.fullmatch(r"JT-\d{4}-\d{4}", ref) is not None, ref)

# --- 3. Choose a period ----------------------------------------------------
status, period = get(f"/kiosk/{ref}/period")
check("period page loads", status == 200)
check("one hour is R150", "R150" in period)
check("two hours is R250", "R250" in period)
check("deposit shown", "R300" in period)
check("one hour total is R450", "R450" in period)
check("two hour total is R550", "R550" in period)

status, location, _ = post(f"/kiosk/{ref}/period", {"plan": "2h"})
check("period accepted", status == 303 and location.endswith("/details"), location)

# --- 4. Details, with validation ------------------------------------------
status, details = get(f"/kiosk/{ref}/details")
check("details page loads", status == 200)
check("consent checkbox present", "hackathon demonstration" in details)

status, _, body = post(f"/kiosk/{ref}/details", {"name": "", "mobile": "1", "email": "nope"})
check("empty form is rejected", status == 200 and "Enter your first name" in body)
check("bad mobile rejected", "valid mobile number" in body)
check("bad email rejected", "valid email address" in body)
check("missing consent rejected", "accept the demo terms" in body)

status, _, body = post(f"/kiosk/{ref}/details", {
    "name": "Demo Customer", "mobile": "071 181 5248",
    "email": "demo@juicetech.co.za",
})
check("consent is required even when the rest is valid", "accept the demo terms" in body)

status, location, _ = post(f"/kiosk/{ref}/details", {
    "name": "Demo Customer", "mobile": "071 181 5248",
    "email": "demo@juicetech.co.za", "consent": "yes",
})
check("valid details accepted", status == 303 and location.endswith("/payment"), location)

# --- 5. Payment method -----------------------------------------------------
status, pay_methods = get(f"/kiosk/{ref}/payment")
check("payment page loads", status == 200)
for label in ["Card", "Capitec Pay", "Apple Pay", "Scan to Pay"]:
    check(f"offers {label}", label in pay_methods)
check("payment options labelled demo", "No real money will be charged" in pay_methods)

status, location, _ = post(f"/kiosk/{ref}/payment", {"method": "card"})
check("method accepted", status == 303 and location.endswith("/pay"), location)

# --- 6. DemoPay screen -----------------------------------------------------
status, pay = get(f"/kiosk/{ref}/pay")
check("DemoPay loads", status == 200)
check("DemoPay heading", "DemoPay" in pay)
check("order reference shown", ref in pay)
check("rental fee shown", "R250" in pay)
check("deposit shown", "R300" in pay)
check("total shown", "R550" in pay)
check("yellow demo banner", "HACKATHON DEMO — NO REAL PAYMENT" in pay)
check("simulate success button", "Simulate Successful Payment" in pay)
check("simulate failure button", "Simulate Failed Payment" in pay)
check("cancel button", "Cancel Payment" in pay)
check("test card number shown", "4111 1111 1111 1111" in pay)
check("warns against real cards", "Do not enter real banking information" in pay)
check("a bank was reserved", re.search(r"PB-\d{3}", pay) is not None)

# The card screen must never offer somewhere to type a real card.
check("no card number input field", 'name="card_number"' not in pay and 'name="cvv"' not in pay)

# --- 7. Scan to Pay --------------------------------------------------------
post(f"/kiosk/{ref}/payment", {"method": "scan"})
status, scan = get(f"/kiosk/{ref}/pay")
check("scan screen loads", status == 200)
check("QR image referenced", f"/kiosk/{ref}/qr.svg" in scan)
check("15 minute countdown", "15:00" in scan)
check("simulate on this device", "Simulate Payment on This Device" in scan)

status, qr = get(f"/kiosk/{ref}/qr.svg")
check("QR svg renders", status == 200 and "<svg" in qr)

# --- 8. Failure path first -------------------------------------------------
status, location, _ = post(f"/kiosk/{ref}/pay/fail", {})
check("failure redirects", status == 303 and location.endswith("/declined"), location)

status, declined = get(f"/kiosk/{ref}/declined")
check("declined message", "No money was charged" in declined)
check("try again offered", "Try Again" in declined)
check("another method offered", "Choose Another Method" in declined)
check("cancel offered", "Cancel Rental" in declined)

_, before = get("/kiosk?station=JUICE-QR-001")
count_before = int(re.search(r"<strong>(\d+)</strong>", before).group(1))
check("stock returned after failure", count_before == 11, str(count_before))

# --- 9. Now succeed --------------------------------------------------------
post(f"/kiosk/{ref}/payment", {"method": "card"})
status, location, _ = post(f"/kiosk/{ref}/pay/success", {})
check("success redirects to dispensing", status == 303 and location.endswith("/dispensing"), location)

status, disp = get(f"/kiosk/{ref}/dispensing")
check("dispensing page loads", status == 200)
check("authorising message", "Authorising demo payment" in disp)
check("payment successful message", "Demo payment successful" in disp)
check("connecting message", "Connecting to Juice Station" in disp)
check("payment confirmed message", "Payment confirmed" in disp)
check("unlocking message", "Unlocking slot" in disp)
check("released message", "Power bank released" in disp)
check("take from flashing slot", "from the flashing slot" in disp)
check("station graphic present", "k-slots" in disp)

bank = re.search(r"(PB-\d{3})", disp).group(1)

status, location, _ = post(f"/kiosk/{ref}/dispensed", {})
check("collect redirects to receipt", status == 303 and location.endswith("/receipt"), location)

# --- 10. Receipt -----------------------------------------------------------
status, receipt = get(f"/kiosk/{ref}/receipt")
check("receipt loads", status == 200)
check("receipt title", "HACKATHON DEMO RECEIPT" in receipt)
check("customer name", "Demo Customer" in receipt)
check("reference", ref in receipt)
check("station id", "JUICE-QR-001" in receipt)
check("power bank", bank in receipt)
check("rental fee", "R250" in receipt)
check("deposit", "R300" in receipt)
check("total", "R550" in receipt)
check("payment status", "PAID — SIMULATED" in receipt)
check("deposit held before return", "Held until return" in receipt)

# --- 11. Return ------------------------------------------------------------
status, ret = get("/return-power-bank")
check("return page loads", status == 200)

status, _, body = post("/return-power-bank", {"reference": "JT-2026-9999", "bank_id": bank})
check("unknown reference rejected", "No rental found" in body)

status, _, body = post("/return-power-bank", {"reference": ref, "bank_id": "PB-999"})
check("wrong power bank rejected", "not PB-999" in body, body[:200])

status, location, _ = post("/return-power-bank", {"reference": ref, "bank_id": bank})
check("return accepted", status == 303 and location.endswith("/done"), location)

status, done = get(f"/return-power-bank/{ref}/done")
check("return confirmation", "Return accepted" in done)
check("insert instruction", "Insert power bank into slot" in done)
check("detected message", "Power bank detected" in done)
check("completed message", "Rental completed" in done)
check("refund message", "deposit refund initiated — SIMULATED" in done)

status, _, body = post("/return-power-bank", {"reference": ref, "bank_id": bank})
check("double return rejected", "already returned" in body)

status, receipt2 = get(f"/kiosk/{ref}/receipt")
check("receipt shows refund", "REFUNDED — SIMULATED" in receipt2)

_, after = get("/kiosk?station=JUICE-QR-001")
count_after = int(re.search(r"<strong>(\d+)</strong>", after).group(1))
check("stock restored after return", count_after == 11, str(count_after))

# --- 12. Dashboard ---------------------------------------------------------
status, dash = get("/demo-dashboard")
check("dashboard loads", status == 200)
check("shows available", "Available" in dash)
check("shows revenue", "Simulated revenue" in dash)
check("shows deposits held", "Deposits held" in dash)
check("shows deposits refunded", "Deposits refunded" in dash)
check("shows station online", "Station online" in dash)
check("lists the rental", ref in dash)
check("has reset control", "Reset demo" in dash)
check("shows battery levels", "k-unit-bar" in dash)

# --- 13. Every screen keeps its demo labelling -----------------------------
for path in [f"/kiosk?station=JUICE-QR-001", f"/kiosk/{ref}/receipt",
             "/return-power-bank", "/demo-dashboard"]:
    _, body = get(path)
    check(f"demo badge on {path}", "Hackathon Demo Mode" in body)
    check(f"disclaimer on {path}", "No real payments are processed" in body)

# --- 14. Reset -------------------------------------------------------------
status, location, _ = post("/demo-dashboard/reset", {})
check("reset redirects", status == 303)
_, dash2 = get("/demo-dashboard")
check("reset clears rentals", ref not in dash2)

status, gone = get(f"/kiosk/{ref}/receipt")
check("cleared rental shows a friendly page", status == 200 and "Rental not found" in gone)

print("=" * 62)
print(f"  {passed} passed, {failed} failed\n")
raise SystemExit(1 if failed else 0)
