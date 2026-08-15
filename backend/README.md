# Juice Tech (Python)

The whole Juice Tech site — pages *and* API — served by Python. Handles
cellphone verification, power bank rentals, late fees, live station
availability, nearest-station lookup and event enquiries.

Built with **FastAPI** + **SQLModel** on **SQLite**, with **Jinja2 HTML
templates, hand-written CSS and vanilla JavaScript** on the front end.

**No build step, no framework, no CDN.** Every asset is served from this
folder, so the site still works when venue wifi does not.

---

## Running it in PyCharm

Pick **Juice Tech** from the run dropdown (top right) and press ▶. That runs
`main.py` in the project root, which starts both halves of the app together.

Individual configurations, if you need to run one piece on its own:

| Configuration | What it does | URL |
|---|---|---|
| `Juice Tech` | **The site + API** — runs `main.py` | http://localhost:8000 |
| `Juice Tech API` | Same thing, started directly by uvicorn | http://localhost:8000 |
| `Page Tests` | Every nav page and internal link loads (50 checks) | — |
| `API Smoke Test` | Walks the whole rental journey (45 checks) | — |
| `Late Fee Tests` | Fee rules only, no server needed (14 checks) | — |
| `Juice Tech Dev Server` | Legacy React site, needs Bun | http://localhost:8080 |

**One-time setup:** point PyCharm at the virtual environment so imports resolve
in the editor — `Settings → Project: Hackathon → Python Interpreter → Add
Interpreter → Existing`, then select:

```
backend\.venv\Scripts\python.exe
```

## Running it from a terminal

```bash
python main.py
```

Or the API on its own:

```bash
cd backend && .venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000
```

## Interactive API docs

FastAPI generates a full, clickable API explorer. Good for demos — you can
run a whole rental live in the browser without writing any code:

**http://localhost:8000/docs**

---

## Folder layout

```
backend/
├── app/
│   ├── main.py          FastAPI app, CORS, static files, startup
│   ├── config.py        Prices, fees, grace period — change prices HERE
│   ├── content.py       All website copy — change wording HERE
│   ├── models.py        Database tables
│   ├── schemas.py       Request/response shapes
│   ├── services.py      Late-fee maths, distance maths, reference codes
│   ├── database.py      SQLite connection + column migrations
│   ├── deps.py          Bearer-token auth
│   ├── seed.py          Demo station network with coordinates
│   └── routers/
│       ├── pages.py       The HTML pages
│       ├── pricing.py     GET  /api/pricing
│       ├── stations.py    GET  /api/stations, /api/stations/nearest
│       ├── otp.py         POST /api/otp/...
│       ├── rentals.py     POST /api/rentals
│       └── enquiries.py   POST /api/enquiries
├── templates/           Jinja2 HTML — one file per page
│   ├── base.html          Shared header, nav and footer
│   ├── index.html         /
│   ├── rent.html          /rent-a-power-bank
│   ├── how-it-works.html  /how-it-works
│   ├── return.html        /return  (find nearest station)
│   ├── services.html      /services
│   ├── event-hire.html    /event-hire
│   ├── advertising.html   /advertising
│   ├── franchising.html   /franchising
│   ├── about.html         /about
│   ├── help-centre.html   /help-centre
│   └── contact.html       /contact
├── static/
│   ├── css/styles.css   Every style, hand-written
│   ├── js/return.js     Nearest-station lookup
│   ├── js/contact.js    Enquiry form
│   └── img/favicon.svg
├── test_pages.py        Every page and link loads (needs server)
├── smoke_test.py        End-to-end rental journey (needs server)
├── test_late_fees.py    Unit tests for fee rules (no server)
├── requirements.txt
└── juicetech.db         Created on first run — delete to reset
```

### Adding a page

1. Add an entry to `NAV` in `app/content.py`
2. Add a route in `app/routers/pages.py`
3. Create the template in `templates/`
4. Run `Page Tests` — it fails if a nav link has no route.

---

## Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/api/health` | — | Liveness check |
| GET | `/api/pricing` | — | Packages, deposit, fees |
| GET | `/api/stations` | — | All stations with live availability |
| GET | `/api/stations/nearest` | — | Closest stations to a lat/lng, sorted |
| GET | `/api/stations/{id}` | — | One station |
| POST | `/api/otp/request` | — | Send an OTP to a cellphone number |
| POST | `/api/otp/verify` | — | Exchange OTP for a session token |
| POST | `/api/rentals` | Bearer | Start a rental, release a power bank |
| GET | `/api/rentals/{ref}` | — | Look up a rental by reference |
| POST | `/api/rentals/{ref}/return` | — | Return a bank, settle late fees |
| GET | `/api/rentals` | Bearer | Rental history for this number |
| POST | `/api/enquiries` | — | Submit an event-hire enquiry |
| GET | `/api/enquiries` | — | List enquiries (staff view) |

### Business rules

- **R150** for 1 hour, **R250** for 2 hours
- **R500** refundable deposit per rental
- **15 minutes** grace after the due time, then **R75 per 30 minutes** started
- Late fees never exceed the **R750** replacement fee
- One active rental per cellphone number
- A power bank may be returned to **any** station, not just where it came from
- A station with **every slot occupied cannot accept a return** — the
  nearest-station lookup filters these out with `?for_return=true`

All of these live in `app/config.py`. Change them there and both the API and
the website update — the site reads its prices from `/api/pricing`.

---

## Demo walkthrough

Open http://localhost:8000/docs and run these in order:

1. `POST /api/otp/request` with `{"phone": "0734072268"}`
   → the response includes `debug_code` (no SMS gateway is wired up yet)
2. `POST /api/otp/verify` with that phone and code → copy the `token`
3. Click **Authorize** at the top of the page and paste the token
4. `POST /api/rentals` with `{"station_id": "JT-CPT-001", "package_id": "1h"}`
   → a power bank is assigned and the homepage card drops by one within 10 seconds
5. `POST /api/rentals/{ref}/return` with `{"station_id": "JT-CPT-002"}`
   → returns it to a different station and settles the bill

---

## Before this goes live

`OTP_DEBUG_RETURN_CODE` in `app/config.py` is **True**, which returns the OTP
in the API response so the flow can be demonstrated without an SMS gateway.
Anyone could log in as any phone number. Set it to `False` and connect a real
SMS provider before this is exposed to the public internet.
