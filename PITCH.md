# Juice Tech — Pitch Pack

GirlCode Hackathon, Cape Town, 16 August 2026.
Presentations 11:00–12:30. Submit by 10:00.

Everything below is grounded in what actually runs. No claim here is
aspirational — if it is in this document, it works in the demo.

---

## The one sentence

> **Juice Tech is a shared power bank network for South Africa, where the AI
> decides which cabinets to fill before they run dry — and which batteries to
> pull before they catch fire.**

Say this first. Nothing before it.

---

## Slide structure (5 slides, ~4 minutes)

Follow **Hook → Problem → Solution → Demo → Impact → Ask.**

### 1. Hook (30 sec)
A flat phone in South Africa is not an inconvenience. It is no taxi fare, no
digital ticket, no way to call for help.

Do **not** open with "we built a website".

### 2. Problem (30 sec)
- Loadshedding means you cannot rely on charging at home.
- A power bank you buy sits flat in a drawer 95% of the time.
- One shared bank serves several people a day instead.

### 3. Solution (30 sec)
Scan a QR on the cabinet, verify by OTP, pay, take a bank, return it to **any**
station. R150 an hour, R250 for two, R300 refundable deposit.

Then the differentiator, in one line:
**"The interesting part isn't the rental. It's that the network predicts itself."**

### 4. Demo (90 sec) — see the script below

### 5. Impact + Ask (45 sec) — say this section slowly

**It is August. This is GirlCode.** Do not skip past that.

> "A phone dying at five in the afternoon is not an inconvenience. It is no
> Bolt, no taxi fare, no shared location, no call to someone who will come
> and fetch you. In this country that is not the same risk for everybody.
>
> Our model's busiest hour across the taxi ranks and campuses is **17:00** —
> exactly when people are trying to get home. So an empty cabinet at Langa
> Taxi Rank at five o'clock is not a stock problem. It is a safety problem.
>
> That is what the forecasting is *for*. It is 21.6% better than guessing
> from last week, and every point of that accuracy is a cabinet that still
> has a bank in it at the hour somebody needs to call a ride.
>
> Around that we built: no ID document, so a rental leaves no trail anyone
> could follow. Cabinets only where there is light and people. Charge held
> back so you can always call. And we track batteries, never the person
> carrying one.
>
> None of this solves gender based violence. We are not going to stand here
> and claim that. It is infrastructure built by people who know that a dead
> battery at the wrong moment, on the wrong walk home, is not a small thing."

Then the ask: what you would do with the prize.

**Why this lands:** every number in it is checkable, and naming the limit
yourself is what separates this from a team stapling a cause onto a product.
Judges have heard the second kind all day.

---

## The demo script — rehearse this exactly

Start with **both** browser tabs already open and the server already running.
Never start a demo by starting a server.

| # | Do this | Say this |
|---|---|---|
| 1 | `/kiosk?station=JUICE-QR-001` | "This is what you get when you scan the cabinet. 11 banks available, live." |
| 2 | Tap **Start Rental** → pick **Two hours** | "R250, plus a R300 refundable deposit. You see the total before you commit — R550." |
| 3 | Tap **Use demo details** → Continue | "No ID number. Ever. A cellphone number is all we ask." |
| 4 | Choose **Card** | "Every payment here is simulated — and look, there is nowhere to type a card. We only *display* the test number. You physically cannot enter a real one." |
| 5 | **Simulate Successful Payment** | *(say nothing — let the dispensing animation play)* |
| 6 | Animation finishes | "Slot 7 unlocks, the bank slides out. That's the customer journey." |
| 7 | **View Demo Receipt** | "Reference, station, bank, deposit status. Printable." |
| 8 | Go to `/ai` | "Now the part that makes this more than a vending machine." |
| 9 | Point at the stat row | "Demand forecast error 2.06 banks per station-hour. The honest baseline — same station, same hour, last week — is 2.63. We're 21.6% better than that." |
| 10 | Change **Stage 0 → Stage 4**, re-run | "Eskom publishes the schedule, so loadshedding is an *input*, not a guess. Watch the forecast move." |
| 11 | Scroll to the van run | "That's tonight's route. And these sites stay short even after the van runs — that's the same model telling us where the next cabinet goes." |
| 12 | Scroll to battery health | "632 batteries scored, AUC 0.863. This one gets pulled before it swells. That's a safety model, not a maintenance one." |
| 13 | In **Ask Juice**, type: `my id is 9001015800083 and my card is 4111 1111 1111 1111` | "Watch what actually leaves the machine." |
| 14 | Point at the green line | "Stripped before transmission. The AI never sees it. That's POPIA by construction, not by promise." |

**Stop there.** Do not show anything else.

---

## Real numbers — only quote these

| Claim | Value |
|---|---|
| Demand forecast MAE | **2.064** rentals per station-hour |
| Naive baseline MAE | **2.633** (same station, same hour, last week) |
| Improvement over baseline | **21.6%** |
| Rows trained on | **25,920** hours of telemetry |
| Training time | **~7 seconds**, on a laptop, offline |
| Battery health AUC | **0.863** across **632** banks |
| Stations modelled | **18** across Cape Town |
| Busiest hour, taxi ranks + campuses | **17:00** — the journey home |
| Forecast rentals in that hour | **82.7** across those 7 sites |
| Automated checks passing | **212** |

Sites in that group, by name: CT Station Taxi Deck, Bellville Taxi Rank,
Langa Taxi Rank, Mitchells Plain Terminus, UCT Upper Campus, CPUT District
Six, Stellenbosch Neelsie.

---

## Judge questions, and the honest answers

**"Why not use an LLM for the forecasting?"**
Because it is the wrong tool. Gradient boosting on tabular telemetry trains in
seconds, runs with no internet, and tells you which feature drove the call. The
language model has one job here: talking to customers.

**"Is the data real?"**
No — it is synthetic, generated from a fixed seed so the demo is identical every
run. `fleet.telemetry()` is the single swap point for real cabinet data; every
model downstream keeps the same signature. We would rather say that plainly than
have you find out.

**"Is the payment real?"**
No, and deliberately so. There is no card input field anywhere in the flow. Every
screen is labelled as a demo.

**"What did you build this weekend?"**
Be honest, per rule 12. The AI models and the policy engine predate this weekend.
Built during the hackathon: the entire Python site and API, the kiosk rental
journey, the nearest-station finder, the AI operations page, and the 208 checks.
State this before anyone asks.

**"Why no framework?"**
Hand-written CSS, no CDN, no build step. If the venue wifi dies mid-demo, the
site still renders. That was a decision, not a limitation.

**"How does this scale?"**
One model across every station with station type as a feature — so a brand new
cabinet forecasts on day one instead of after two months of its own history.
That is the difference between expanding into Delft and not bothering.

**"Isn't the safety angle a stretch for a power bank company?"**
The honest answer, and do not get defensive: we are not claiming to prevent
assault. We are saying a phone is how you call a ride, share a location, or
reach someone — and it dies at the worst possible time. The model's peak hour
across taxi ranks and campuses is 17:00. We built the forecasting so a cabinet
is stocked at that hour, and the privacy design so renting leaves no trail. If
that reads as a stretch, look at what we removed: no ID, no card stored, no
tracking of the person. Those cost us conversion. We did them anyway.

---

## Before you present

- [ ] Server running, both tabs open, **demo reset done** (`/demo-dashboard` → Reset)
- [ ] `/ai` loaded **once already** — first load trains the models and takes ~7s
- [ ] Phone on the same wifi if showing mobile
- [ ] **Backup screen recording** of the full journey, in case the laptop fails
- [ ] Rehearsed end to end **at least 5 times**
- [ ] Know who says which section

## If something breaks

Do not apologise or debug on stage. Say:
> "That's the demo gremlin — here's the recording, and I'll walk you through it."

Then play the backup video and keep talking.

---

## What we would do next

- Swap `fleet.telemetry()` for real cabinet check-ins. Nothing downstream changes.
- Connect a real payment provider and SMS gateway (`OTP_DEBUG_RETURN_CODE = False`).
- Pilot at one taxi rank and one campus, and measure whether the forecast holds.
