# Juice Tech Hub

**Pay for the time, share the power.** A South African shared power bank
network — rentals, event charging and digital advertising.

---

## Quick start

You need **Python 3.10 or newer**. Nothing else — no Node, no npm, no build step.

```bash
git clone https://github.com/Asemahlezide22/juicetech-hackathon.git
cd juicetech-hackathon
python main.py
```

**Ubuntu and macOS: the command is `python3 main.py`.** Plain `python` usually
does not exist there. On Windows, try `py main.py` if `python` is not on PATH.

**Ubuntu only, once:** Debian and Ubuntu ship the venv module separately from
Python, so install it before the first run or the setup step fails:

```bash
sudo apt install python3-venv
```

The first run creates `backend/.venv` and installs dependencies automatically
(about a minute). Every run after that starts immediately.

Then open:

| | |
|---|---|
| **The site** | http://localhost:8000 |
| **API documentation** | http://localhost:8000/docs |

Press `Ctrl+C` to stop.

### Opening it on a phone

The station QR is meant to be scanned, which only works if a phone can reach
the machine serving the site. Startup prints the address to use:

```
On your phone (same wifi):  http://10.40.18.124:8000
```

Open the site at **that** address rather than `localhost`, then scan the code
on `/how-it-works`. The QR is generated per request from the address the page
was loaded at, so a page opened at `localhost` would otherwise produce a code
pointing at the phone itself. Loopback is swapped for the network address
automatically, but opening the right address keeps every other link correct too.

Two things commonly block this, neither of them the site's fault:

- **Windows Firewall.** A network classified *Public* drops inbound
  connections. Allow the port from an Administrator PowerShell, and remove the
  rule afterwards:

  ```powershell
  New-NetFirewallRule -DisplayName "Juice Tech demo" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Public -RemoteAddress LocalSubnet
  ```

- **Client isolation.** Guest and venue wifi often stops devices talking to
  each other at all. Nothing on the laptop can fix that — use a phone hotspot,
  or put the site behind a tunnel.

The server binds `0.0.0.0` so that any of this can work. That means everyone
on the network can reach it, which is the point at a demo and not something to
leave running on a café connection.

### Running the tests

With the site running, in a second terminal:

```bash
cd backend
python test_pages.py
```

| Suite | Checks | Needs the server? |
|---|---|---|
| `test_pages.py` | 107 — every page, link and asset; colour mode; the menu | yes |
| `test_kiosk.py` | 111 — the kiosk demo, pricing and payment states | yes |
| `smoke_test.py` | 45 — the full rental journey end to end | yes |
| `test_late_fees.py` | 14 — late-fee rules | no |

277 checks in total.

Each script re-launches itself under `backend/.venv`, so any Python works —
`python`, `python3` or `py`, whichever your system has.

### Opening it in PyCharm

Open this folder, then pick **Juice Tech** from the run dropdown and press ▶.

### The site

Eight pages, defined once in `backend/app/content.py` as `NAV`. Every entry
needs a matching route in `backend/app/routers/pages.py`, and a test fails if
one is missing.

| | |
|---|---|
| `/` | Home |
| `/rent-a-power-bank` | Rent a Power Bank |
| `/how-it-works` | How It Works — carries the scannable station QR |
| `/return` | Return — finds your nearest station |
| `/event-hire` | Event Hire |
| `/safety` | Safety — the reason the project exists |
| `/about` | About Us |
| `/contact` | Contact Us |

Not in the navigation, but part of the demo:

| | |
|---|---|
| `/kiosk?station=JUICE-QR-001` | What a scanned cabinet opens |
| `/demo-dashboard` | The presenter's view, including **Reset Demo** |

### What is where

```
main.py       Start everything. The only file you need to run.
backend/      The entire app — Python API + HTML pages. See backend/README.md.
src/          The original React build. No longer used; kept for reference.
```

`backend/README.md` documents the API, the business rules and how to add a page.

### Things worth knowing before changing the CSS

- **Colour mode.** Light and dark, switched by the button in the header, and
  following the device until someone presses it. Every colour that moves is a
  token at the top of `styles.css`; the fixed brand colours above them do not
  move. Two rules exist that must not be "tidied up": the QR keeps a literal
  white plate in both themes, because a code on a dark background will not
  scan, and gold-as-text uses `--accent-text`, which darkens on a light page
  because `#ffd400` on white is about 1.5:1.
- **The navigation** is a row above 860px and a menu behind a button below it.
  The breakpoint is written in both `styles.css` and `site.js`; if they ever
  disagree, the nav hides on a screen with no button to bring it back.
- **Nothing may depend on JavaScript to become visible.** Sections are visible
  by default and the scroll-reveal effect is armed by a script, not the other
  way round, so a failed script leaves a readable page. There are tests
  pinning all of this.

### The old React site

Superseded by the Python build, but still runnable if you have
[Bun](https://bun.sh) installed:

```bash
python main.py --with-react
```

---

# Juice Tech — the original build brief

> **This is history, not documentation.** Everything below is the brief the
> first version of this site was generated from. It is kept because it records
> where the project started, and because the hackathon rules ask for AI use to
> be disclosed. It is **not** a description of what exists now — read it as the
> original ask, and the section above as the current state.
>
> Where the built site deliberately differs:
>
> | The brief says | What was built | Why |
> |---|---|---|
> | R500 refundable deposit | **R300** | Lowered so the demo price is realistic for the market it serves |
> | Advertising, Franchising, Help Centre and Services pages | Removed | Four pages of text nobody reads in a seven-minute pitch |
> | An FAQ section | Replaced by the AI chat assistant | Same answers, asked in your own words |
> | A staff login and password-protected dashboard | Open `/demo-dashboard` | A judge cannot be asked for a password mid-demo |
> | React, Vite and a component library | Plain HTML, CSS and Python | No build step and no CDN, so the site still renders when the venue wifi fails |
> | — | A safety page, and a colour mode | Added: the GBV angle is the point of the project, not a feature of the brief |

**How to use this:** Copy everything below the line into a single prompt in Lovable.ai or Bolt.ai. Both tools work best with one long, structured prompt like this rather than several short ones — paste it as your first message to start the build.

---

Build a modern, mobile-first website and web app for **Juice Tech**, a South African smart power bank rental, event charging and digital advertising business.

## BRAND IDENTITY & LOGO

**Business name:** Juice Tech

**Primary tagline:** "Pay for the time, share the power."

**Secondary tagline (use in supporting copy/meta descriptions):** "Stay Powered. Stay Limitless."

**Logo brief — design and generate this as a clean, scalable SVG logo, not a placeholder:**
- Concept: a bold lightning bolt merged with a battery/power-cell outline, forming a monogram that reads as "JT" at a glance. The lightning bolt should feel energetic and fast; the battery shape should feel solid and trustworthy.
- Style: geometric, modern, flat — no gradients, no 3D effects, no stock icon look. Think "confident startup" not "clip art."
- Colour version: electric yellow/gold bolt on black, for the primary lockup.
- Also generate a reversed version: black or white bolt on transparent/white background, for use on light sections and station screens.
- Deliver the logo as inline SVG components so it renders crisply at any size — favicon, navbar, station-screen display, and large hero use.
- Pair the icon with the wordmark "Juice Tech" in a bold, geometric sans-serif (see typography below). The wordmark and icon should work both combined (icon + text lockup) and as a standalone icon (for favicon/app icon use).

**Do not use a generic bolt-in-a-circle clip-art icon.** Make the mark distinctive enough that it wouldn't be mistaken for any other charging or energy brand.

## VISUAL DESIGN DIRECTION — MAKE THIS LOOK GENUINELY GOOD, NOT TEMPLATED

This is important: don't default to a generic SaaS-template look (centered hero, stock gradient blob, generic rounded-card grid with no hierarchy). Aim for something that feels designed — energetic, confident, and premium, like a well-funded startup's site, not a hackathon MVP.

**Colour palette:**
- Black (`#0A0A0A` or similar near-black, not pure `#000`) — primary background for hero and bold sections
- Electric yellow/gold (`#FFD400`–`#F5C400` range) — primary accent, call-to-action colour
- White (`#FFFFFF`) — primary content backgrounds
- Soft grey (`#F4F4F5`/`#E8E8EA` range) — secondary content backgrounds, card fills
- Use black and yellow with real intent (backgrounds, dividers, icon fills) rather than yellow only on buttons — the palette should feel woven through the whole site, not bolted on

**Typography:**
- Bold, geometric, confident sans-serif for headings (something in the spirit of Space Grotesk, General Sans, or Inter with heavy weights) — headings should feel like they have presence, not default browser-safe fallback fonts
- Clean, highly legible sans-serif for body copy, sized generously — this app will be used quickly, often outdoors, sometimes one-handed, so err toward larger text and high contrast over dense small type

**Layout and interaction:**
- Rounded cards (consistent radius system — don't mix radii randomly)
- Battery and lightning-bolt iconography used consistently as a visual motif (progress indicators, loading states, section dividers)
- Smooth, purposeful micro-animations — button hover states, card entrance on scroll, a subtle pulse/charge animation on the live station card — but nothing gratuitous or slow enough to feel like it's blocking the user
- Yellow call-to-action buttons with strong contrast, black text on yellow (not white on yellow — check contrast)
- Black hero sections, white/light-grey content sections, alternating rhythm down the page so it doesn't feel flat
- High contrast and accessible text throughout (WCAG AA minimum) — this matters both for accessibility and because this app will be used on bright outdoor screens at events
- Real photography/illustration of a charging station and power bank in use where possible (hero image), not generic stock-photo-of-people-laughing-at-a-laptop

The site must work well and look intentional on:
- Mobile phones (this is the primary use case — most users will be scanning a QR code on their phone at an event)
- Tablets
- Desktop computers
- Charging-station screens (these are large, often viewed from a distance — a station-screen "kiosk" mode should use larger text and simpler layout)

## BUSINESS DESCRIPTION

Juice Tech allows users to rent fast-charging portable power banks from smart charging stations at events, venues and public spaces.

Users scan a QR code, verify their cellphone number, choose a rental period, pay securely, collect a power bank and continue moving around while their phone charges.

Juice Tech helps users remain connected so they can call loved ones, order transport, access digital tickets, make payments, capture content and contact help when needed.

The charging stations also have large digital screens that can display paid advertisements, event information, sponsor messages, safety notices and Juice Tech instructions.

## PUBLIC WEBSITE NAVIGATION

1. Home
2. Rent a Power Bank
3. How It Works
4. Services
5. Event Hire
6. Advertising
7. Franchising
8. About Us
9. Help Centre
10. Contact Us
11. Staff Login

## HOME PAGE

Create a hero section with:

**Heading:** "Never let a low battery end your experience."

**Subheading:** "Rent a fast-charging Juice Tech power bank, stay connected and keep moving. Pay for the time, share the power."

**Primary button:** "Rent Now"

**Secondary button:** "Book Juice Tech for an Event"

Include an image of a Juice Tech charging station in the hero (generate/use a clean product-style render or photo-style illustration of a black-and-yellow charging cabinet).

Show a live station card with:
- Station online
- Number of power banks available
- Number currently rented
- Fast charging available
- Scan QR code to begin

Add homepage sections for:
- The problem Juice Tech solves
- How renting works
- Safety and connectivity
- Event hire
- Digital advertising
- Franchising
- Frequently asked questions
- Contact details

## HOW RENTING WORKS

Display the following steps:

1. Scan the QR code on the Juice Tech station
2. Enter and verify your cellphone number using OTP
3. Choose a rental package
4. Pay securely
5. Collect the assigned power bank
6. Charge while moving around
7. Return the power bank to a Juice Tech station
8. Receive a return confirmation and receipt

## CUSTOMER RENTAL PRICING

- 1 hour: R150
- 2 hours: R250

Before payment, clearly show:
- Rental fee
- Rental duration
- Refundable security deposit
- Return deadline
- Late-return fee
- Replacement charge
- Terms and conditions checkbox

## SECURITY DEPOSIT

Use a configurable refundable deposit of R500 for the demo.

The deposit must be refunded or released once the correct power bank is successfully returned.

Show a notice that bank processing times may affect when the refund reflects.

## CUSTOMER QR RENTAL FLOW

Each charging station must have a unique QR code linked to a station ID.

When scanned:
1. Open `/rent/{stationId}`
2. Confirm the station exists
3. Confirm the station is online
4. Display the venue name and available power banks
5. Ask for the user's cellphone number
6. Send an OTP
7. Verify the OTP
8. Ask the user to select:
   - R150 for 1 hour
   - R250 for 2 hours
9. Show the security deposit and terms
10. Process payment
11. Create a unique rental order number
12. Send a command to the charging-station API to release a power bank
13. Save the battery ID and slot ID
14. Start the rental timer
15. Show the active rental screen
16. Send the customer a receipt by email or SMS
17. Send reminders before expiry
18. Confirm the return through the station API or webhook
19. End the rental
20. Calculate any late fees
21. Release or refund the deposit
22. Send a return confirmation

## ACTIVE RENTAL SCREEN

Show:
- Customer name
- Rental reference
- Power-bank ID
- Station collected from
- Rental start time
- Selected package
- Time remaining
- Return deadline
- Current estimated total
- Return instructions
- Extend Rental button
- Find a Return Station button
- Report a Problem button
- Contact Support button

## PAYMENT OPTIONS

Use Payfast as the main payment gateway.

Display these payment options where supported:
- Debit card
- Credit card
- Capitec Pay
- Instant EFT
- Apple Pay
- Google Pay
- QR payment

Also include an in-person payment option for staffed events using:
- Tap to pay
- Chip and PIN
- Mobile wallets

Use sandbox or demo payment mode during development.

Do not store raw card details.

Use:
- Hosted checkout
- Secure payment verification
- Payment success callback
- Payment failure callback
- Refund flow
- Webhook verification
- Duplicate payment prevention
- Idempotency keys

## THEFT AND LOSS PREVENTION

Create a layered security system using:
- OTP cellphone verification
- Successful payment before release
- Refundable R500 deposit
- Unique customer-to-battery assignment
- Unique battery ID
- Unique station ID
- Unique slot ID
- Unique order number
- Rental timer
- Automated reminders
- Account blocking for overdue rentals
- Staff alerts
- Audit logs

Send reminders:
- 15 minutes before expiry
- At expiry
- 30 minutes overdue
- Final overdue notice

Do not allow a user with an overdue power bank to rent another one.

**Power-bank statuses:** Available, Reserved, Released, Active rental, Returned, Charging, Low battery, Overdue, Missing, Damaged, Maintenance, Blocked.

**Suggested late fee:** R75 for every additional 30 minutes after a 15-minute grace period. Late fees must not exceed the disclosed replacement value.

**Suggested replacement fee:** Make it configurable. Default demo value: R750. Require staff review before charging a replacement fee.

## POWER-BANK CABINET API

Use this base URL:

```
https://api.w-dian.cn/operate
```

Keep all API credentials on the server only. Use environment variables for: operator account, password, token, ocode.

**Authentication:** `POST /auth/login` — automatically refresh the API session when the token expires or when a 401 response is received.

**Cabinet API endpoints to use:**
- Add cabinet: `POST /equipment/add`
- Edit cabinet: `POST /equipment/edit`
- Get cabinet information: `POST /equipment/info`
- Delete cabinet: `POST /equipment/delete`
- List cabinets: `GET /equipment/index?page=1`
- Battery list: `GET /equipment/batteryList?page=1`
- Issue cabinet instruction: `POST /equipment/operate`
- Get current cabinet and power-bank details: `POST /equipment/detail`

**Power-bank release:** After successful payment, send a server-side request to `POST /equipment/operate` including `cabinet_id`, `type = borrow`, `lock_id` where needed, and a unique `order_no`. Save `battery_id`, `lock_id`, response result, and timestamp. Do not mark the rental as active until the API confirms a successful release.

**Station monitoring:** Use the API to display cabinet ID, model, online/offline status, last heartbeat, signal level, slot number, battery ID, battery charge percentage, quick-charge status, available units, and empty return slots. Do not release a power bank below the minimum battery level set by staff.

**Return webhook:** Create a secure HTTPS return webhook. When a power bank is returned: verify the event, match the battery ID to an active rental, save the return station and slot, end the rental, calculate final charges, mark the battery as returned, release or refund the deposit, send the customer a return receipt, update dashboard data, and log the action. Prevent duplicate webhook processing.

## DIGITAL ADVERTISING API

Use these API endpoints:

- Advertising materials: `POST /screenadv/addMaterial`, `POST /screenadv/deleteMaterial`, `POST /screenadv/materialList?page=1`
- Advertising groups: `POST /screenadv/addGroup`, `POST /screenadv/editGroup`, `POST /screenadv/deleteGroup`, `POST /screenadv/groupDetail`, `GET or POST /screenadv/groupList?page=1`
- Advertising plans: `POST /screenadv/addPlan`, `POST /screenadv/editPlan`, `POST /screenadv/deletePlan`, `POST /screenadv/plandetail`, `GET or POST /screenadv/planList?page=1`

Allow authorised staff to: upload image or video adverts, name the advertiser, select campaign dates, select venues, select charging stations, choose display hours, set display duration, arrange advert order, preview campaigns, approve or reject content, pause campaigns, view active campaigns, record campaign revenue, and record estimated impressions.

Uploaded advert files must use secure HTTPS URLs.

## STAFF LOGIN

Create secure role-based access with these roles: Super Administrator, Operations Manager, Finance, Customer Support, Venue Manager, Advertising Manager, Franchise Owner, Read-only Analyst.

Include: email and password login, password reset, optional two-factor authentication, session timeout, role permissions, audit logs.

## STAFF DASHBOARD

Create a dashboard with summary cards for: today's rental revenue, event-hire revenue, advertising revenue, total revenue, active rentals, completed rentals, overdue rentals, failed payments, pending refunds, available power banks, rented power banks, charging power banks, missing power banks, online stations, offline stations, new enquiries, open support tickets, active advertising campaigns, franchise leads.

Include charts for: revenue by day/week/month, rentals by hour, rental package popularity, station performance, venue performance, payment methods, return rate, overdue rate, advertising income, battery utilisation, franchise performance.

**Dashboard menu:** Overview, Rentals, Payments, Refunds and Deposits, Stations, Power Banks, Venues, Customers, Event Bookings, Advertising, Enquiries, Support Tickets, Franchise Leads, Reports, Staff and Permissions, Pricing Settings, System Settings, Audit Logs.

**Rentals table columns:** rental reference, customer, masked cellphone number, venue, station ID, battery ID, rental package, start time, return deadline, return time, payment status, rental status, deposit status, total charge, staff actions.

Allow staff to search and filter by: rental reference, cellphone number, battery ID, station, venue, date, payment status, rental status.

## SERVICES PAGE

List: power-bank rentals, event charging solutions, charging-station hire, digital screen advertising, sponsored charging stations, venue partnerships, corporate activations, branded power banks, event reporting, franchise opportunities.

## EVENT-HIRE PAGE

Create a section called **"Bring Juice Tech to Your Event."**

**Small Event Package — R3,500**
One station, up to 8 hours, 12 power banks, delivery within Cape Town, setup and collection, remote monitoring.

**Standard Event Package — R5,500**
One station, up to 12 hours, 12–24 power banks, digital advertising screen, setup and collection, remote monitoring.

**Premium Event Package — R8,500**
Two stations, up to 12 hours, up to 48 power banks, advertising screens, setup and collection, one on-site support assistant.

**Large Event Package — From R15,000**
Multiple stations, 48+ power banks, on-site support, sponsor branding, event reporting, custom quote.

**Weekend Hire Package — From R10,500**
One station Friday–Sunday, up to 24 power banks, remote monitoring, setup and collection.

**Optional extras:**
- Additional station: R2,500–R3,500/day
- Additional 12 power banks: R1,500/day
- On-site assistant: R1,800 for up to 8 hours
- Additional staff hour: R250/hour
- Custom station branding: from R1,500
- Advert displayed on screen: from R1,000/event
- Exclusive screen sponsorship: R3,500–R7,500/event
- Detailed post-event report: R750
- Delivery outside central Cape Town: custom quote
- Overnight or multi-day event: custom quote

Add this note: *"Prices are launch estimates and may change depending on the event location, duration, number of guests, equipment required, staffing and branding."*

**Alternative revenue-share option** (for venues/organisers who don't want an upfront fee): Juice Tech installs the station at a reduced or no upfront venue fee; venue receives 20% of net rental revenue; Juice Tech keeps the remaining net rental revenue; advertising income remains with Juice Tech unless agreed otherwise. Explain that "net rental revenue" means rental income after approved refunds and payment-processing fees.

**Event-hire form fields:** full name, company name, email, contact number, event type, event date, start time, end time, venue, expected attendance, number of stations required, number of power banks required, advertising-screen requirement, branding requirement, on-site staff requirement, additional notes.

After submission: save the enquiry, generate a reference number, send confirmation to the customer, send an alert to `info@juicetech.co.za`, create a dashboard task, mark the enquiry as New, send a reminder if not assigned within two business hours.

## ADVERTISING PAGE

Create packages and an advertising enquiry form. Explain that advertisers can display: brand adverts, sponsor messages, event schedules, food and beverage promotions, transport information, QR-code campaigns, safety information, emergency announcements.

**Advertising enquiry fields:** name, company, email, contact number, campaign dates, preferred venue, number of stations, budget range, image or video upload, enquiry message.

## FRANCHISING PAGE

**Heading:** "Power your city with Juice Tech."

Explain that Juice Tech can assist franchise partners with: charging stations, power banks, business model, technology platform, training, operating processes, sales support, venue acquisition guidance, marketing material, advertising sales model, dashboard access, maintenance guidance.

**Franchise enquiry fields:** full name, company name, province, city, email, contact number, available investment range, business experience, preferred territory, message.

Include this notice: *"Submitting an enquiry does not guarantee franchise approval or the award of a territory."*

## ABOUT US PAGE

Use this text (adapted):

*"Juice Tech was created after experiencing the frustration and risk of having a phone battery die when it was needed most. We believe that access to power helps people remain connected, capture important moments, arrange transport and stay in touch with loved ones. Juice Tech combines portable charging, smart technology and digital advertising to create safer and more convenient experiences — because when you pay for the time, you get to share the power with the people and moments that matter."*

Include: Mission, Vision, Founder story, Safety impact, Technology, Venue partnerships, South African growth plans.

## CONTACT PAGE

**Email:** info@juicetech.co.za
**Telephone and WhatsApp:** 073 407 2268
**Location:** Sea Point, Cape Town, 8005

**Contact form fields:** name, company name, email, contact number, enquiry type, enquiry message, consent checkbox.

After submission: save the enquiry, generate a reference number, send an acknowledgement email, send the enquiry to `info@juicetech.co.za`, create a dashboard ticket, track response time, escalate overdue enquiries.

## EMAIL ENQUIRY AUTOMATION

Integrate the website with the `info@juicetech.co.za` inbox using a transactional email provider such as Resend, SendGrid, Mailgun, or Microsoft Graph.

Create automated templates for: general enquiry acknowledgement, event-hire enquiry, advertising enquiry, franchise enquiry, rental receipt, return confirmation, refund initiated, rental expiry reminder, overdue notice, payment failed, support ticket confirmation.

For incoming emails: match replies to an existing enquiry using reference numbers and email addresses, add emails to the enquiry timeline, create a new enquiry when no match exists, show unread status, notify assigned staff, allow staff to reply from the dashboard, track first response time, prevent duplicate email records.

## AI CHATBOT

Add a Juice Tech AI support chatbot that answers questions about: rental prices, how renting works, payment options, returns, security deposits, late returns, event hire, advertising, franchising, contact information, station locations.

The chatbot must: use only approved Juice Tech information, never invent station availability, escalate payment disputes, escalate safety concerns, offer a "Talk to a Person" option, create a support ticket when needed.

**WhatsApp escalation:** Whenever the chatbot offers "Talk to a Person," escalates a payment dispute, escalates a safety concern, or cannot resolve a query, it must direct the user to WhatsApp **062 372 6017** (e.g. "Chat to our team directly on WhatsApp: 062 372 6017" with a tap-to-chat `https://wa.me/27623726017` link where possible). Show this same number/link as a persistent option in the chat widget, not only as a fallback message.

## HELP CENTRE

Create articles for: how to rent, how to return, payment methods, security deposit and refunds, late returns, lost or damaged power banks, station did not release a power bank, payment succeeded but no power bank was released, event bookings, advertising, franchising, privacy, contacting support.

## CUSTOMER RENTAL TERMS

Include a terms-and-conditions page with:

1. Users must be at least 18 years old or use the service through a parent or guardian.
2. Rental prices are R150 for one hour and R250 for two hours.
3. The rental begins once the station releases the power bank.
4. A refundable deposit may be required.
5. The power bank must be returned by the deadline shown.
6. A 15-minute grace period may apply.
7. Late fees may be charged after the grace period.
8. The return is complete only once the station confirms it.
9. Users must contact support if the return is not confirmed.
10. Users may be responsible for deliberate damage, misuse or failure to return the power bank.
11. Normal wear and tear is not chargeable.
12. Users may not open, alter, sell, transfer or remove labels from the power bank.
13. Juice Tech does not store raw card details.
14. Failed releases must be investigated and refunded or corrected.
15. Users must stop using a power bank that becomes damaged, wet, swollen or unusually hot.
16. Personal information is processed according to the privacy policy.
17. Disputed charges must be reviewed using payment, rental and station records.
18. Terms accepted at the start of a rental apply to that rental.

## EVENT-HIRE TERMS

Include: booking confirmed after quotation acceptance and payment; 50% deposit to confirm; remaining 50% payable five business days before the event; full payment required for late bookings; cancellation rules; safe installation area required; suitable electricity required; venue permission required; safe access for delivery and collection; Juice Tech retains ownership of all equipment; organiser may be responsible for damage caused by staff or unsafe venue conditions; customer rental revenue arrangements must be agreed in writing; advertising content must be lawful and approved; internet and network interruptions may affect service; additional staff hours are chargeable; delivery outside Cape Town may cost extra.

## DATABASE

Create tables for: users, staff, roles, venues, stations, station_slots, power_banks, rentals, rental_packages, payments, deposits, refunds, payment_webhooks, station_events, enquiries, enquiry_messages, support_tickets, event_bookings, advertisers, advertising_materials, advertising_groups, advertising_campaigns, franchise_leads, notifications, audit_logs, system_settings.

## RECOMMENDED TECHNOLOGY

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** Next.js server routes or Node.js
- **Database:** Supabase or PostgreSQL
- **Authentication:** Supabase Auth, Clerk or Firebase Auth
- **Storage:** Supabase Storage, AWS S3 or Cloudinary
- **Hosting:** Vercel

## DEMO MODE

Create a complete hackathon demo with: mock Juice Tech station, 12 demo power banks, simulated OTP, simulated Payfast payment, simulated API release, live countdown timer, simulated return webhook, deposit refund status, rotating digital adverts, populated staff dashboard, demo enquiries, demo franchise leads.

Clearly label all simulated transactions as **Demo** or **Test**.

## FINAL OUTPUT

Generate:
- Public Juice Tech website with the custom logo and full brand identity described above
- Mobile QR rental journey
- Customer rental interface
- Staff dashboard
- Event-hire page and pricing
- Advertising management
- Franchise enquiry system
- Contact and enquiry management
- Email automation
- AI chatbot
- Database schema
- API service layer
- Environment variable template
- Test data
- Setup instructions

**Reminder on quality:** this needs to look like a polished, fundable product, not a hackathon prototype — invest real effort in the logo, the hero section, and consistent spacing/typography before moving on to secondary pages.

This project was built with [Lovable](https://lovable.dev).

**Live app**: https://charge-and-go-share.lovable.app

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/979489a6-dfb2-49cd-ad20-7292d05791a2).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
