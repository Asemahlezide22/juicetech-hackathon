export const BRAND = {
  name: "Juice Tech",
  tagline: "Pay for the time, share the power.",
  taglineAlt: "Stay Powered. Stay Limitless.",
  email: "info@juicetech.co.za",
  phone: "073 407 2268",
  phoneHref: "tel:+27734072268",
  whatsapp: "062 372 6017",
  whatsappHref: "https://wa.me/27623726017",
  location: "Sea Point, Cape Town, 8005",
};

export const NAV = [
  { label: "Home", to: "/" },
  { label: "Rent a Power Bank", to: "/rent-a-power-bank" },
  { label: "How It Works", to: "/how-it-works" },
  { label: "Services", to: "/services" },
  { label: "Event Hire", to: "/event-hire" },
  { label: "Advertising", to: "/advertising" },
  { label: "Franchising", to: "/franchising" },
  { label: "About Us", to: "/about" },
  { label: "Help Centre", to: "/help-centre" },
  { label: "Contact Us", to: "/contact" },
] as const;

export const PACKAGES = [
  { id: "1h", label: "1 Hour", minutes: 60, price: 150 },
  { id: "2h", label: "2 Hours", minutes: 120, price: 250 },
] as const;

export const DEPOSIT = 500;
export const REPLACEMENT_FEE = 750;
export const LATE_FEE_PER_30 = 75;
export const GRACE_MINUTES = 15;

export const RENT_STEPS = [
  "Scan the QR code on the Juice Tech station",
  "Enter and verify your cellphone number using OTP",
  "Choose a rental package",
  "Pay securely",
  "Collect the assigned power bank",
  "Charge while moving around",
  "Return the power bank to a Juice Tech station",
  "Receive a return confirmation and receipt",
];

export const EVENT_PACKAGES = [
  {
    name: "Small Event",
    price: "R3,500",
    features: [
      "One station",
      "Up to 8 hours",
      "12 power banks",
      "Delivery within Cape Town",
      "Setup and collection",
      "Remote monitoring",
    ],
  },
  {
    name: "Standard Event",
    price: "R5,500",
    featured: true,
    features: [
      "One station",
      "Up to 12 hours",
      "12–24 power banks",
      "Digital advertising screen",
      "Setup and collection",
      "Remote monitoring",
    ],
  },
  {
    name: "Premium Event",
    price: "R8,500",
    features: [
      "Two stations",
      "Up to 12 hours",
      "Up to 48 power banks",
      "Advertising screens",
      "Setup and collection",
      "One on-site support assistant",
    ],
  },
  {
    name: "Large Event",
    price: "From R15,000",
    features: [
      "Multiple stations",
      "48+ power banks",
      "On-site support",
      "Sponsor branding",
      "Event reporting",
      "Custom quote",
    ],
  },
  {
    name: "Weekend Hire",
    price: "From R10,500",
    features: [
      "One station Friday–Sunday",
      "Up to 24 power banks",
      "Remote monitoring",
      "Setup and collection",
    ],
  },
];

export const EVENT_EXTRAS = [
  ["Additional station", "R2,500 – R3,500 / day"],
  ["Additional 12 power banks", "R1,500 / day"],
  ["On-site assistant", "R1,800 for up to 8 hours"],
  ["Additional staff hour", "R250 / hour"],
  ["Custom station branding", "from R1,500"],
  ["Advert displayed on screen", "from R1,000 / event"],
  ["Exclusive screen sponsorship", "R3,500 – R7,500 / event"],
  ["Detailed post-event report", "R750"],
  ["Delivery outside central Cape Town", "Custom quote"],
  ["Overnight or multi-day event", "Custom quote"],
];

export const FAQS = [
  {
    q: "How much does it cost to rent a power bank?",
    a: "R150 for one hour and R250 for two hours. A refundable R500 security deposit is held and released once the power bank is returned.",
  },
  {
    q: "How do I start a rental?",
    a: "Scan the QR code on any Juice Tech station, verify your cellphone number with an OTP, choose your package, pay securely and collect the power bank the station releases for you.",
  },
  {
    q: "Which cables are included?",
    a: "Every Juice Tech power bank has built-in Micro-USB, USB-C and Lightning cables, so you don't need to carry your own.",
  },
  {
    q: "What happens if I return it late?",
    a: "A 15-minute grace period applies. After that a late fee of R75 per additional 30 minutes may be charged, capped at the disclosed replacement value.",
  },
  {
    q: "When do I get my deposit back?",
    a: "The deposit is released as soon as the station confirms the correct power bank has been returned. Bank processing times may affect when the refund reflects in your account.",
  },
  {
    q: "Can I hire Juice Tech for my event?",
    a: "Yes. Packages start at R3,500 for a single station for up to 8 hours, including delivery, setup, collection and remote monitoring within Cape Town.",
  },
];

export const HELP_ARTICLES = [
  ["How to rent", "Scan the station QR code, verify your number, choose a package, pay and collect the power bank released to you."],
  ["How to return", "Slide the power bank into any empty slot at a Juice Tech station until it clicks. Wait for the on-screen confirmation."],
  ["Payment methods", "Debit and credit cards, Capitec Pay, Instant EFT, Apple Pay, Google Pay and QR payment via Payfast. Staffed events also accept tap to pay and chip and PIN."],
  ["Security deposit and refunds", "A refundable R500 deposit is held for each rental and released on confirmed return. Bank processing can take a few working days."],
  ["Late returns", "A 15-minute grace period applies, then R75 per additional 30 minutes. Late fees never exceed the disclosed replacement value."],
  ["Lost or damaged power banks", "A configurable replacement fee applies (currently R750). Every replacement charge is reviewed by staff first."],
  ["Station did not release a power bank", "Do not pay again. Contact support with your rental reference — failed releases are investigated and refunded or corrected."],
  ["Payment succeeded but no power bank released", "Your rental stays inactive until the station confirms a release, so the charge is reversed or a bank is released manually."],
  ["Event bookings", "Submit the event hire form and you'll receive a reference number plus a quotation. Bookings confirm on a 50% deposit."],
  ["Advertising", "Upload image or video creative, choose venues, stations and display hours. All content is approved before going live."],
  ["Franchising", "Juice Tech supplies equipment, technology, training and sales support to approved franchise partners."],
  ["Privacy", "Personal information is processed according to our privacy policy. Juice Tech never stores raw card details."],
  ["Contacting support", "Email info@juicetech.co.za, call 073 407 2268 or WhatsApp 062 372 6017."],
];

export const DEMO_STATION = {
  id: "JT-CPT-001",
  venue: "Sea Point Promenade Market",
  online: true,
  available: 9,
  rented: 3,
  total: 12,
  fastCharge: true,
  signal: 4,
};
