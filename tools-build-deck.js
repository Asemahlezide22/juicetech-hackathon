const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";              // 13.3 x 7.5
pres.author = "Juice Tech";
pres.title = "Juice Tech — GirlCode Hackathon 2026";

// Brand palette. Yellow dominates, black carries it, white for type.
const Y = "FFD400";
const Y_SOFT = "FFE775";
const BLACK = "080808";
const PANEL = "16161C";
const PANEL_2 = "1E1E26";
const WHITE = "FFFFFF";
const DIM = "B6B6C2";
const GREEN = "5BD67F";

const H = "Arial";        // headings
const B = "Calibri";      // body

const dark = { color: BLACK };

/** Repeated motif: a yellow disc with a glyph, used beside every section head. */
function disc(slide, x, y, glyph, size = 0.52) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: size, h: size, fill: { color: Y },
  });
  slide.addText(glyph, {
    x, y, w: size, h: size,
    align: "center", valign: "middle",
    fontFace: H, fontSize: 15, bold: true, color: BLACK, margin: 0,
  });
}

function card(slide, x, y, w, h, fill = PANEL) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.12,
    fill: { color: fill },
    line: { color: "2C2C36", width: 1 },
  });
}

/* ------------------------------------------------------------------ 1 title */
{
  const s = pres.addSlide();
  s.background = dark;

  s.addShape(pres.ShapeType.ellipse, {
    x: 9.4, y: -1.6, w: 6.2, h: 6.2, fill: { color: "1A1705" },
  });

  s.addText("JUICE TECH", {
    x: 0.9, y: 1.5, w: 9, h: 0.9,
    fontFace: H, fontSize: 54, bold: true, color: Y, charSpacing: 2, margin: 0,
  });

  s.addText("Pay for the time, share the time.", {
    x: 0.9, y: 2.4, w: 9, h: 0.5,
    fontFace: B, fontSize: 20, color: DIM, margin: 0,
  });

  s.addText(
    "A shared power bank network for South Africa, where the AI decides which " +
    "cabinets to fill before they run dry — and which batteries to pull before " +
    "they catch fire.",
    { x: 0.9, y: 3.3, w: 8.6, h: 1.4,
      fontFace: B, fontSize: 18, color: WHITE, lineSpacing: 28, margin: 0 }
  );

  s.addText("GirlCode Hackathon  ·  Cape Town  ·  August 2026", {
    x: 0.9, y: 6.3, w: 9, h: 0.4,
    fontFace: B, fontSize: 13, color: DIM, margin: 0,
  });

  s.addNotes(
    "Open with the one sentence, nothing before it. Then say: it is August, " +
    "this is GirlCode, and the problem we picked is one our team knows."
  );
}

/* ---------------------------------------------------------------- 2 problem */
{
  const s = pres.addSlide();
  s.background = { color: "FAFAFA" };

  disc(s, 0.9, 0.75, "1");
  s.addText("The problem", {
    x: 1.6, y: 0.72, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: "7A6A00", charSpacing: 1.5, margin: 0,
  });

  s.addText("A flat phone strands you.", {
    x: 0.9, y: 1.3, w: 11.5, h: 0.9,
    fontFace: H, fontSize: 40, bold: true, color: BLACK, margin: 0,
  });

  const items = [
    ["No way home", "No taxi fare, no e-hailing, no ticket."],
    ["No way to call", "No help, no shared location, no emergency number."],
    ["Loadshedding", "You cannot rely on charging at home."],
  ];
  items.forEach(([t, d], i) => {
    const x = 0.9 + i * 3.95;
    card(s, x, 2.6, 3.6, 1.9, "FFFFFF");
    s.addText(t, {
      x: x + 0.28, y: 2.85, w: 3.05, h: 0.4,
      fontFace: H, fontSize: 18, bold: true, color: BLACK, margin: 0,
    });
    s.addText(d, {
      x: x + 0.28, y: 3.3, w: 3.05, h: 1,
      fontFace: B, fontSize: 14, color: "4A4A55", lineSpacing: 20, margin: 0,
    });
  });

  s.addText(
    "Buying a power bank does not fix it. It spends most of its life flat, in a " +
    "drawer. One shared bank serves several people a day instead.",
    { x: 0.9, y: 5.0, w: 11.5, h: 0.9,
      fontFace: B, fontSize: 17, color: "3A3A45", lineSpacing: 26, margin: 0 }
  );

  s.addNotes("Thirty seconds. Do not linger — the next slide is the one that matters.");
}

/* ------------------------------------------------------- 3 the 17:00 moment */
{
  const s = pres.addSlide();
  s.background = dark;

  disc(s, 0.9, 0.75, "2");
  s.addText("Why it matters", {
    x: 1.6, y: 0.72, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: Y, charSpacing: 1.5, margin: 0,
  });

  s.addText("17:00", {
    x: 0.9, y: 1.4, w: 4.2, h: 1.7,
    fontFace: H, fontSize: 96, bold: true, color: Y, margin: 0,
  });
  s.addText("Our model's busiest hour across the taxi ranks and campuses.", {
    x: 0.9, y: 3.1, w: 4.6, h: 1.1,
    fontFace: B, fontSize: 16, color: WHITE, lineSpacing: 24, margin: 0,
  });

  s.addText(
    [
      { text: "That is when people are trying to get home.\n", options: { bold: true, color: WHITE } },
      { text: "So an empty cabinet at Langa Taxi Rank at five o'clock is not a " +
              "stock problem. It is a safety problem.\n\n", options: { color: DIM } },
      { text: "In South Africa that risk is not the same for everybody. A phone " +
              "is how you call a ride, share a location, or reach someone who " +
              "will come and fetch you.", options: { color: DIM } },
    ],
    { x: 5.9, y: 1.5, w: 6.5, h: 3.4,
      fontFace: B, fontSize: 17, lineSpacing: 27, margin: 0 }
  );

  card(s, 5.9, 5.1, 6.5, 1.15, PANEL_2);
  s.addText(
    "None of this solves gender based violence. It is infrastructure built by " +
    "people who know that a dead battery at the wrong moment is not a small thing.",
    { x: 6.2, y: 5.3, w: 5.9, h: 0.8,
      fontFace: B, fontSize: 13, italic: true, color: Y_SOFT, lineSpacing: 19, margin: 0 }
  );

  s.addNotes(
    "Slow down here. Land 17:00 as a fact, not a plea. Say the limitation out " +
    "loud — naming it is what separates us from stapling a cause onto a product."
  );
}

/* ----------------------------------------------------- 4 demand curve chart */
{
  const s = pres.addSlide();
  s.background = { color: "FAFAFA" };

  disc(s, 0.9, 0.75, "3");
  s.addText("The forecast", {
    x: 1.6, y: 0.72, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: "7A6A00", charSpacing: 1.5, margin: 0,
  });
  s.addText("Demand peaks exactly when the walk home starts.", {
    x: 0.9, y: 1.25, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: BLACK, margin: 0,
  });

  const hours = ["00","01","02","03","04","05","06","07","08","09","10","11",
                 "12","13","14","15","16","17","18","19","20","21","22","23"];
  const values = [0,0,0,0,1.0,13.9,33.3,37.4,30.5,55.0,46.9,47.1,51.2,55.0,
                  54.1,66.2,80.3,82.7,61.4,44.0,23.9,13.0,4.2,2.4];

  s.addChart(
    pres.ChartType.bar,
    [{ name: "Forecast rentals", labels: hours, values }],
    {
      x: 0.9, y: 2.1, w: 11.5, h: 3.5,
      barDir: "col",
      chartColors: [Y],
      showTitle: false,
      showLegend: false,
      showValue: false,
      catAxisLabelColor: "6A6A75",
      catAxisLabelFontSize: 10,
      catAxisLabelFontFace: B,
      valAxisLabelColor: "6A6A75",
      valAxisLabelFontSize: 10,
      valAxisLabelFontFace: B,
      valGridLine: { color: "E2E2E6", size: 1 },
      catGridLine: { style: "none" },
      barGapWidthPct: 40,
    }
  );

  s.addText(
    "Hourly forecast across 7 taxi rank and campus sites — Langa, Mitchells Plain, " +
    "Bellville, CT Station Taxi Deck, UCT, CPUT, Stellenbosch. Peak 82.7 rentals at 17:00.",
    { x: 0.9, y: 5.75, w: 11.5, h: 0.7,
      fontFace: B, fontSize: 12, color: "6A6A75", lineSpacing: 18, margin: 0 }
  );

  s.addNotes("This is real model output, not a mock. Point at the 17:00 bar.");
}

/* ------------------------------------------------------------- 5 the models */
{
  const s = pres.addSlide();
  s.background = dark;

  disc(s, 0.9, 0.7, "4");
  s.addText("The AI", {
    x: 1.6, y: 0.67, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: Y, charSpacing: 1.5, margin: 0,
  });
  s.addText("Four models. Three are not language models.", {
    x: 0.9, y: 1.2, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: WHITE, margin: 0,
  });

  const models = [
    ["Demand forecasting", "Gradient boosting", "2.064 MAE",
     "vs 2.633 guessing from last week — 21.6% better, 25 920 rows, trained in 7 seconds"],
    ["Battery health", "Gradient boosting classifier", "0.863 AUC",
     "632 banks scored, 42 flagged to pull before they swell. A safety model, not maintenance"],
    ["Rebalancing", "Constrained allocation", "8 vs 171",
     "At stage 4 the van moves 8 banks and 171 stay short — that is where the next cabinet goes"],
    ["Concierge", "LLM + retrieval", "5 languages",
     "Grounded in our published policies. Every message redacted before it leaves the device"],
  ];

  models.forEach(([name, kind, metric, body], i) => {
    const x = 0.9 + (i % 2) * 5.9;
    const y = 2.15 + Math.floor(i / 2) * 2.35;
    card(s, x, y, 5.5, 2.05);
    s.addText(name, {
      x: x + 0.3, y: y + 0.2, w: 3.2, h: 0.35,
      fontFace: H, fontSize: 16, bold: true, color: WHITE, margin: 0,
    });
    s.addText(metric, {
      x: x + 3.3, y: y + 0.17, w: 2.0, h: 0.4,
      fontFace: H, fontSize: 19, bold: true, color: Y, align: "right", margin: 0,
    });
    s.addText(kind, {
      x: x + 0.3, y: y + 0.58, w: 4.9, h: 0.3,
      fontFace: B, fontSize: 12, color: Y_SOFT, margin: 0,
    });
    s.addText(body, {
      x: x + 0.3, y: y + 0.93, w: 4.9, h: 1,
      fontFace: B, fontSize: 12.5, color: DIM, lineSpacing: 18, margin: 0,
    });
  });

  s.addNotes(
    "If asked why not an LLM for forecasting: gradient boosting on tabular " +
    "telemetry trains in seconds, runs offline, and tells you which feature " +
    "drove the call. The language model has one job — talking to humans."
  );
}

/* ------------------------------------------------------------- 6 the safety */
{
  const s = pres.addSlide();
  s.background = { color: "FAFAFA" };

  disc(s, 0.9, 0.75, "5");
  s.addText("Designed around it", {
    x: 1.6, y: 0.72, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: "7A6A00", charSpacing: 1.5, margin: 0,
  });
  s.addText("Decisions that cost us conversion.", {
    x: 0.9, y: 1.25, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: BLACK, margin: 0,
  });

  const rows = [
    ["No ID document, ever",
     "A cellphone number verified by OTP is all we ask. Renting leaves nothing behind that could be used to find you."],
    ["Cabinets only where there is light",
     "Lit, staffed, overlooked locations, reviewed with the host. A cabinet in a dark corner is a mugging waiting to happen."],
    ["Charge held back for the trip home",
     "Get Home mode will not let your charge fall below what it takes to call a ride."],
    ["We track batteries, not people",
     "The bank is our property, so we know where it is. We do not follow the person carrying it."],
  ];

  rows.forEach(([t, d], i) => {
    const y = 2.2 + i * 1.02;
    s.addShape(pres.ShapeType.ellipse, {
      x: 0.9, y: y + 0.06, w: 0.34, h: 0.34, fill: { color: Y },
    });
    s.addText(t, {
      x: 1.45, y, w: 4.4, h: 0.45,
      fontFace: H, fontSize: 16, bold: true, color: BLACK, margin: 0,
    });
    s.addText(d, {
      x: 5.9, y: y - 0.02, w: 6.5, h: 0.9,
      fontFace: B, fontSize: 13.5, color: "4A4A55", lineSpacing: 19, margin: 0,
    });
  });

  s.addText("POPIA-native, by construction rather than by policy.", {
    x: 0.9, y: 6.4, w: 11.5, h: 0.4,
    fontFace: B, fontSize: 14, italic: true, color: "6A6A75", margin: 0,
  });

  s.addNotes("Say the ID one out loud. Removing it has a cost — we did it anyway.");
}

/* ---------------------------------------------------------------- 7 product */
{
  const s = pres.addSlide();
  s.background = dark;

  disc(s, 0.9, 0.7, "6");
  s.addText("The product", {
    x: 1.6, y: 0.67, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: Y, charSpacing: 1.5, margin: 0,
  });
  s.addText("Scan, pay, go. Return it anywhere.", {
    x: 0.9, y: 1.2, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: WHITE, margin: 0,
  });

  const steps = [
    ["01", "Scan", "the QR on the cabinet"],
    ["02", "Verify", "your number by OTP"],
    ["03", "Pay", "and collect your bank"],
    ["04", "Return", "to any free slot"],
  ];
  steps.forEach(([n, t, d], i) => {
    const x = 0.9 + i * 2.95;
    card(s, x, 2.2, 2.65, 1.85);
    s.addText(n, {
      x: x + 0.28, y: 2.4, w: 2.1, h: 0.5,
      fontFace: H, fontSize: 24, bold: true, color: Y, margin: 0,
    });
    s.addText(t, {
      x: x + 0.28, y: 2.95, w: 2.1, h: 0.35,
      fontFace: H, fontSize: 17, bold: true, color: WHITE, margin: 0,
    });
    s.addText(d, {
      x: x + 0.28, y: 3.33, w: 2.15, h: 0.6,
      fontFace: B, fontSize: 12.5, color: DIM, lineSpacing: 17, margin: 0,
    });
  });

  const prices = [
    ["R150", "one hour"],
    ["R250", "two hours"],
    ["R300", "refundable deposit"],
    ["18", "stations modelled"],
  ];
  prices.forEach(([v, l], i) => {
    const x = 0.9 + i * 2.95;
    s.addText(v, {
      x, y: 4.6, w: 2.65, h: 0.6,
      fontFace: H, fontSize: 34, bold: true, color: Y, margin: 0,
    });
    s.addText(l, {
      x, y: 5.2, w: 2.65, h: 0.35,
      fontFace: B, fontSize: 13, color: DIM, margin: 0,
    });
  });

  s.addText(
    "Built in Python — FastAPI, SQLModel, hand-written CSS. No framework, no CDN, " +
    "no build step: the site still renders when the venue wifi dies.",
    { x: 0.9, y: 6.1, w: 11.5, h: 0.8,
      fontFace: B, fontSize: 14, color: DIM, lineSpacing: 21, margin: 0 }
  );

  s.addNotes("Keep this short — the demo shows it better than the slide does.");
}

/* ------------------------------------------------------------------- 8 demo */
{
  const s = pres.addSlide();
  s.background = { color: "FAFAFA" };

  disc(s, 0.9, 0.75, "7");
  s.addText("Live demo", {
    x: 1.6, y: 0.72, w: 6, h: 0.5,
    fontFace: B, fontSize: 15, bold: true, color: "7A6A00", charSpacing: 1.5, margin: 0,
  });
  s.addText("What you are about to see.", {
    x: 0.9, y: 1.25, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: BLACK, margin: 0,
  });

  card(s, 0.9, 2.2, 5.6, 3.9, "FFFFFF");
  s.addText("The customer", {
    x: 1.2, y: 2.45, w: 5, h: 0.4,
    fontFace: H, fontSize: 18, bold: true, color: BLACK, margin: 0,
  });
  s.addText(
    [
      { text: "Scan the cabinet QR — 11 banks, live", options: { bullet: true, breakLine: true } },
      { text: "Choose two hours, see R550 before committing", options: { bullet: true, breakLine: true } },
      { text: "No ID asked for, ever", options: { bullet: true, breakLine: true } },
      { text: "Pay — simulated, and there is nowhere to type a card", options: { bullet: true, breakLine: true } },
      { text: "Slot 7 unlocks, the bank slides out", options: { bullet: true, breakLine: true } },
      { text: "Receipt, then return it to a different station", options: { bullet: true } },
    ],
    { x: 1.2, y: 2.95, w: 5, h: 3,
      fontFace: B, fontSize: 14, color: "3A3A45", paraSpaceAfter: 8, margin: 0 }
  );

  card(s, 6.8, 2.2, 5.6, 3.9, "FFFFFF");
  s.addText("The network", {
    x: 7.1, y: 2.45, w: 5, h: 0.4,
    fontFace: H, fontSize: 18, bold: true, color: BLACK, margin: 0,
  });
  s.addText(
    [
      { text: "Move Eskom stage 0 to 4 — the forecast moves", options: { bullet: true, breakLine: true } },
      { text: "Tonight's van route, and what it cannot fix", options: { bullet: true, breakLine: true } },
      { text: "The battery flagged to pull before it swells", options: { bullet: true, breakLine: true } },
      { text: "Type an ID and card number into the assistant", options: { bullet: true, breakLine: true } },
      { text: "Watch what actually leaves the machine", options: { bullet: true } },
    ],
    { x: 7.1, y: 2.95, w: 5, h: 3,
      fontFace: B, fontSize: 14, color: "3A3A45", paraSpaceAfter: 8, margin: 0 }
  );

  s.addText("208 automated checks pass across four suites.", {
    x: 0.9, y: 6.35, w: 11.5, h: 0.4,
    fontFace: B, fontSize: 14, italic: true, color: "6A6A75", margin: 0,
  });

  s.addNotes(
    "Ninety seconds. Golden path only. If anything breaks, do not debug — " +
    "switch to the recording and keep talking."
  );
}

/* -------------------------------------------------------------- 9 close/ask */
{
  const s = pres.addSlide();
  s.background = dark;

  s.addShape(pres.ShapeType.ellipse, {
    x: -1.8, y: 3.6, w: 6.4, h: 6.4, fill: { color: "1A1705" },
  });

  s.addText("What we would do next", {
    x: 0.9, y: 0.9, w: 11.5, h: 0.6,
    fontFace: H, fontSize: 30, bold: true, color: WHITE, margin: 0,
  });

  const next = [
    ["Swap the data", "fleet.telemetry() is the single swap point for real cabinet check-ins. Nothing downstream changes."],
    ["Connect the rails", "A real payment provider and SMS gateway. The flow is already built around them."],
    ["Pilot and measure", "One taxi rank, one campus. Does the forecast hold against real demand?"],
  ];
  next.forEach(([t, d], i) => {
    const y = 1.9 + i * 1.15;
    s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: y + 0.05, w: 0.34, h: 0.34, fill: { color: Y } });
    s.addText(t, {
      x: 1.45, y, w: 3.3, h: 0.4,
      fontFace: H, fontSize: 16, bold: true, color: WHITE, margin: 0,
    });
    s.addText(d, {
      x: 4.9, y: y - 0.02, w: 7.5, h: 0.9,
      fontFace: B, fontSize: 13.5, color: DIM, lineSpacing: 19, margin: 0,
    });
  });

  card(s, 0.9, 5.5, 11.5, 1.25, PANEL_2);
  s.addText("Pay for the time, share the time.", {
    x: 1.25, y: 5.72, w: 6.5, h: 0.45,
    fontFace: H, fontSize: 22, bold: true, color: Y, margin: 0,
  });
  s.addText("juicetech.co.za  ·  Sea Point, Cape Town", {
    x: 1.25, y: 6.17, w: 6.5, h: 0.35,
    fontFace: B, fontSize: 13, color: DIM, margin: 0,
  });
  s.addText("Thank you", {
    x: 8.6, y: 5.85, w: 3.4, h: 0.5,
    fontFace: H, fontSize: 24, bold: true, color: WHITE, align: "right", margin: 0,
  });

  s.addNotes(
    "State plainly, per rule 12: the AI models and policy engine predate this " +
    "weekend. Built during the hackathon — the whole Python site and API, the " +
    "kiosk rental journey, the nearest-station finder, the safety page and the " +
    "208 checks. Then the ask."
  );
}

pres.writeFile({ fileName: "C:/dev/juicetech-hackathon/Juice-Tech-Pitch.pptx" })
  .then(f => console.log("wrote", f));
