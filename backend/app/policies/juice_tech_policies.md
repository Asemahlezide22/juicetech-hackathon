# Juice Tech — Customer Policies

*Pay for the time, share the power.*

These are the documents the AI concierge is grounded in. If the assistant cannot
find an answer here, it is instructed to say so and hand over to a human rather
than invent one.

---

## 1. Pricing

- **One hour costs R150. Two hours cost R250.** You choose the package before
  the cabinet releases a bank, so you know the price before you commit.
- A **refundable R300 deposit** is held for the duration of the rental and
  released as soon as a cabinet confirms the correct bank has come back. Bank
  processing can take a few working days to reflect.
- **A 15-minute grace period** applies after your time is up. After that, a late
  fee of **R75 per additional 30 minutes** may be charged.
- Late fees are **capped at the R750 replacement value** and can never exceed it,
  so the worst case is disclosed before you start.
- **Prices never rise during load shedding.** There is no surge multiplier in our
  pricing engine at any Eskom stage. Charging people more the moment the lights
  go out is not a business we are willing to run.
- Pay by card, EFT, SnapScan, or cash voucher bought from the host site. Cash
  vouchers exist because roughly one in five adults in South Africa still
  transacts mainly in cash, and they should not be locked out of a charge.

## 2. Returns

- Return the bank to **any Juice Tech cabinet**, not only the one you took it from.
- The clock stops the moment the cabinet accepts the unit and the slot latches.
- If every slot at a cabinet is full, the app opens the nearest cabinet with
  space and **freezes your billing** while you walk there. You are not charged
  for our capacity problem.
- If a bank is never returned, the **R750 replacement fee** applies and the
  deposit is set against it. That figure is disclosed upfront and is the ceiling
  on what a rental can ever cost you. We would rather sell you the unit than send
  a debt collector after a student.

## 3. Privacy (POPIA)

Juice Tech processes personal information under the **Protection of Personal
Information Act 4 of 2013 (POPIA)**, and is accountable to the Information
Regulator of South Africa.

**What we collect**

- A mobile number, used to open and close a rental.
- Payment confirmation — a token from the payment provider. We never see or
  store your card number, expiry, or CVV.
- Rental events: which cabinet, which battery, start time, end time.

**What we deliberately do not collect**

- **No ID number.** You do not need a green book or a smart card to charge a phone.
- **No card details on our servers.** Tokenised at the payment provider only.
- **No location tracking of you.** We know where the *battery* is, because it is
  our property. We do not follow the person carrying it, and the app requests
  location only while it is open and only to list nearby cabinets.
- **No contacts, photos, microphone, or storage permissions.** The app does not
  ask for them because it does not need them.
- **No selling or sharing** of personal information with advertisers or data
  brokers. Ever. Not as a current policy — as a term of this contract.

**Your rights under POPIA**

You may ask us what we hold on you, correct it, or delete it. Reply DELETE on
WhatsApp or email privacy@juicetech.co.za. We action deletion within 7 days and
confirm in writing.

**Retention.** Rental records are kept for 12 months for billing disputes and
fraud, then automatically deleted. Mobile numbers are hashed after an account is
closed.

**Breach.** If personal information is ever compromised, we notify affected
customers and the Information Regulator, as section 22 of POPIA requires.

**Where the data lives.** In South African data centres. Cross-border transfer of
personal information is restricted under section 72 of POPIA, and we avoid the
question entirely by not exporting it.

## 4. Safety — your phone

**Our cables carry power only. They cannot carry data.**

A USB-A connector has four pins: two for power, two for data. In every Juice
Tech cable the two data pins are **physically absent** — not disabled in
software, not blocked by a setting, simply not there. There is no electrical
path along which a file, an app, or malware could travel between the cabinet and
your phone. This is the same principle as a "USB data blocker", built into the
cable itself so a customer cannot accidentally opt out of it.

This matters because "juice jacking" — a compromised public charging port
attacking a connected phone — is a real, documented attack class, and public
charging lockers are exactly the sort of infrastructure it targets. The FBI's
Denver field office publicly warned travellers about free public USB ports in
2023. Our answer is not a warning label. It is a cable that is physically
incapable of the attack.

Additionally:

- Cabinets run **no user-facing software** on the charging path. The cabinet's
  controller talks to our servers over a one-way telemetry link and has no
  ability to address a connected phone.
- We do not offer a **wireless** charging pad, which would introduce a pairing
  surface we cannot make equally provable.
- Every cable is **captive** — tethered into the bank and impossible to swap for
  a tampered one. A cable that a stranger can substitute is the real weak point
  in shared charging, and we removed it.

## 5. Safety — the battery

- Every unit is **QR-serialised** and its charge and discharge history is tracked
  from the day it enters the fleet.
- **JuiceBrain Health**, our on-fleet model, scores each battery for failure risk
  from cycle count, capacity fade, internal resistance, peak temperature, charge
  faults, and physical swelling. Units above threshold are **pulled before they
  fail**, not after.
- Cabinets are **fused per slot** and have thermal cut-outs. One bad cell cannot
  take a cabinet with it.
- Units carry **SABS-recognised** cell protection circuitry: over-charge,
  over-discharge, over-current, and short-circuit protection.
- Pulled units are bench-tested at the depot. Roughly four in five are refurbished
  into a second service life. The remainder go to a **licensed e-waste recycler**
  with a certificate of destruction, never to landfill.

## 6. Safety — the person

- Cabinets are placed in **lit, staffed, overlooked locations**, and site
  selection is reviewed with the host. A cabinet in a dark corner is a mugging
  waiting to happen and we will not install one.
- **No ID document and no credit check.** A cellphone number verified by OTP is
  all we ask for, so a rental leaves no paper trail that could put someone at
  risk. The refundable deposit is held against the bank, not against your
  identity.
- The app has a **Get Home** mode: it will not let your remaining charge fall
  below the level needed to call a ride or a family member, and it will tell you
  the nearest cabinet on your route rather than the nearest one overall.

## 7. Accessibility

- Works over **USSD** (`*134*JUICE#`) and **WhatsApp**, so a feature phone with no
  data can still rent.
- The app is under 5 MB and functions **offline** for return and pricing lookups.
- Concierge answers in **English, isiXhosa, Afrikaans, isiZulu, and Sesotho**.

## 8. For organisations and event hosts

- Cabinets can be **branded** and pre-paid, so attendees charge free and the host
  covers the tab.
- Hosts receive **anonymised, aggregated** footfall and dwell analytics —
  cabinet-level counts only. No individual customer data is ever passed to a
  host, sponsor, or advertiser.
- Standard commission to the host site is **25% of gross rental revenue**.
- Pop-up cabinets deploy in under 20 minutes and run on internal battery with
  LTE backhaul, so they work at an outdoor festival with no mains and no wifi.

---

*Questions this document does not answer should be escalated to a human at
help@juicetech.co.za or on WhatsApp. The assistant is instructed not to guess.*
