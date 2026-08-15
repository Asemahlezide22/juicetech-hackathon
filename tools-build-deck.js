const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";              // 13.3 x 7.5
pres.author = "Juice Tech";
pres.title = "Juice Tech — GirlCode Hackathon 2026";

const Y = "FFD400";
const BLACK = "080808";
const PANEL = "16161C";
const PANEL_2 = "1E1E26";
const WHITE = "FFFFFF";
const DIM = "B6B6C2";
const LIGHT = "FAFAFA";

const H = "Arial";
const B = "Calibri";

const dark = { color: BLACK };

function card(slide, x, y, w, h, fill = PANEL) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.12,
    fill: { color: fill },
    line: { color: fill === PANEL || fill === PANEL_2 ? "2C2C36" : "E4E4E8", width: 1 },
  });
}

function dot(slide, x, y, size = 0.3) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: size, h: size, fill: { color: Y } });
}

/* --------------------------------------------------------------- 1  title */
{
  const s = pres.addSlide();
  s.background = dark;
  s.addShape(pres.ShapeType.ellipse, { x: 9.2, y: -1.8, w: 6.6, h: 6.6, fill: { color: "1A1705" } });

  s.addText("JUICE TECH", {
    x: 0.9, y: 2.4, w: 10, h: 1.1,
    fontFace: H, fontSize: 60, bold: true, color: Y, charSpacing: 2, margin: 0,
  });
  s.addText("Pay for the time, share the power.", {
    x: 0.95, y: 3.5, w: 10, h: 0.6,
    fontFace: B, fontSize: 24, color: DIM, margin: 0,
  });
  s.addText("GirlCode Hackathon  ·  Cape Town  ·  August 2026", {
    x: 0.95, y: 6.4, w: 10, h: 0.4,
    fontFace: B, fontSize: 13, color: "6A6A75", margin: 0,
  });

  s.addNotes(
    "Say the one sentence and nothing before it:\n\n" +
    "\"Juice Tech is a shared power bank network for South Africa, where the AI " +
    "decides which cabinets to fill before they run dry — and which batteries to " +
    "pull before they catch fire.\"\n\n" +
    "Then: it is August, this is GirlCode, and the problem we picked is one we know."
  );
}

/* --------------------------------------------------------------- 2  scene */
{
  const s = pres.addSlide();
  s.background = dark;
  s.addShape(pres.ShapeType.ellipse, { x: 8.0, y: -2.4, w: 9.5, h: 9.5, fill: { color: "16130A" } });

  s.addText("18:40", {
    x: 0.9, y: 1.5, w: 6, h: 1.6,
    fontFace: H, fontSize: 88, bold: true, color: Y, margin: 0,
  });
  s.addText("Cape Town Station taxi deck.", {
    x: 0.95, y: 3.05, w: 7, h: 0.5,
    fontFace: B, fontSize: 21, color: DIM, margin: 0,
  });
  s.addText("Her phone died an hour ago.", {
    x: 0.9, y: 4.0, w: 7.5, h: 0.8,
    fontFace: H, fontSize: 34, bold: true, color: WHITE, margin: 0,
  });

  card(s, 9.0, 2.6, 3.4, 2.2, PANEL_2);
  s.addText("3%", {
    x: 9.0, y: 3.1, w: 3.4, h: 1.2,
    fontFace: H, fontSize: 64, bold: true, color: "FF6B6B", align: "center", margin: 0,
  });

  s.addNotes(
    "TELL this, do not read it. Pause after the line.\n\n" +
    "She cannot call her sister to say which taxi she is on. Cannot share her " +
    "location. Cannot check if the last one has gone. It is a forty minute trip " +
    "and nobody knows she is making it.\n\n" +
    "Say 'picture this' — it is a scenario, not a testimonial.\n\n" +
    "About 45 seconds."
  );
}

/* ---------------------------------------------------------------- 3  turn */
{
  const s = pres.addSlide();
  s.background = { color: LIGHT };

  s.addText("The cabinet had a bank in it", {
    x: 0.9, y: 2.1, w: 11.5, h: 0.9,
    fontFace: H, fontSize: 40, color: "3A3A45", margin: 0,
  });
  s.addText("because a model said it would be needed.", {
    x: 0.9, y: 3.0, w: 11.5, h: 0.9,
    fontFace: H, fontSize: 40, bold: true, color: BLACK, margin: 0,
  });

  s.addText("Busiest forecast hour: 17:00 — when everybody is going home.", {
    x: 0.9, y: 4.4, w: 11.5, h: 0.5,
    fontFace: B, fontSize: 19, color: "5A5A66", margin: 0,
  });

  s.addNotes(
    "This is the hinge — the story becomes the technology. Land the bold line " +
    "and stop for a beat.\n\n" +
    "An empty cabinet at Langa at five o'clock is not a stock problem. It is a " +
    "safety problem.\n\n" +
    "Then say the limit out loud: 'None of this solves gender based violence, " +
    "and we are not going to stand here and say it does.' Naming it yourself is " +
    "what separates this from stapling a cause onto a product."
  );
}

/* ------------------------------------------------------------ 4  forecast */
{
  const s = pres.addSlide();
  s.background = { color: LIGHT };

  s.addText("Demand peaks when the walk home starts.", {
    x: 0.9, y: 0.7, w: 11.5, h: 0.7,
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
      x: 0.9, y: 1.7, w: 11.5, h: 4.2,
      barDir: "col",
      chartColors: [Y],
      showTitle: false, showLegend: false, showValue: false,
      catAxisLabelColor: "6A6A75", catAxisLabelFontSize: 11, catAxisLabelFontFace: B,
      valAxisLabelColor: "6A6A75", valAxisLabelFontSize: 11, valAxisLabelFontFace: B,
      valGridLine: { color: "E4E4E8", size: 1 },
      catGridLine: { style: "none" },
      barGapWidthPct: 35,
    }
  );

  s.addText("Real model output. 7 taxi rank and campus sites.", {
    x: 0.9, y: 6.05, w: 11.5, h: 0.4,
    fontFace: B, fontSize: 13, color: "6A6A75", margin: 0,
  });

  s.addNotes(
    "Point at the 17:00 bar. Say: this is real output, not a mock.\n\n" +
    "Sites: Langa, Mitchells Plain, Bellville, CT Station Taxi Deck, UCT, CPUT, " +
    "Stellenbosch. Peak 82.7 rentals.\n\n" +
    "Eskom publishes the loadshedding schedule, so stage is an input to the " +
    "model, not something it has to guess. About 45 seconds."
  );
}

/* -------------------------------------------------------------- 5  the AI */
{
  const s = pres.addSlide();
  s.background = dark;

  s.addText("Four models.", {
    x: 0.9, y: 0.7, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 34, bold: true, color: WHITE, margin: 0,
  });
  s.addText("Three of them are not language models.", {
    x: 0.9, y: 1.35, w: 11.5, h: 0.5,
    fontFace: B, fontSize: 18, color: DIM, margin: 0,
  });

  const models = [
    ["2.064", "Demand forecast error", "21.6% better than baseline"],
    ["0.863", "Battery failure AUC", "632 banks scored"],
    ["171", "Banks short at stage 4", "where the next cabinet goes"],
    ["5", "Languages", "answers from our own policies"],
  ];
  models.forEach(([metric, label, sub], i) => {
    const x = 0.9 + i * 2.95;
    card(s, x, 2.4, 2.65, 2.5);
    s.addText(metric, {
      x: x + 0.25, y: 2.7, w: 2.15, h: 0.8,
      fontFace: H, fontSize: 40, bold: true, color: Y, margin: 0,
    });
    s.addText(label, {
      x: x + 0.25, y: 3.55, w: 2.15, h: 0.6,
      fontFace: H, fontSize: 14, bold: true, color: WHITE, margin: 0,
    });
    s.addText(sub, {
      x: x + 0.25, y: 4.1, w: 2.15, h: 0.7,
      fontFace: B, fontSize: 11.5, color: DIM, lineSpacing: 16, margin: 0,
    });
  });

  s.addText("Gradient boosting, trained in 7 seconds. Runs with no internet.", {
    x: 0.9, y: 5.4, w: 11.5, h: 0.5,
    fontFace: B, fontSize: 16, color: DIM, margin: 0,
  });

  s.addNotes(
    "If asked why not an LLM for forecasting: it is the wrong tool. Gradient " +
    "boosting on tabular telemetry trains in seconds, runs offline, and tells " +
    "you which feature drove the call. The language model has one job — talking " +
    "to humans.\n\n" +
    "At stage 4 the van can only move 8 banks because nothing has surplus. 171 " +
    "stay short. That is the model saying: you need another cabinet, not another " +
    "van trip. About 60 seconds."
  );
}

/* -------------------------------------------------------------- 6  safety */
{
  const s = pres.addSlide();
  s.background = { color: LIGHT };

  s.addText("Decisions that cost us conversion.", {
    x: 0.9, y: 0.8, w: 11.5, h: 0.8,
    fontFace: H, fontSize: 34, bold: true, color: BLACK, margin: 0,
  });

  const rows = [
    "No ID document. Ever.",
    "Cabinets only where there is light.",
    "Charge held back for the trip home.",
    "We track batteries, not people.",
  ];
  rows.forEach((t, i) => {
    const y = 2.2 + i * 0.95;
    dot(s, 0.95, y + 0.12);
    s.addText(t, {
      x: 1.55, y, w: 10.5, h: 0.55,
      fontFace: H, fontSize: 24, color: BLACK, margin: 0,
    });
  });

  s.addText("POPIA by construction, not by policy.", {
    x: 0.9, y: 6.2, w: 11.5, h: 0.4,
    fontFace: B, fontSize: 16, italic: true, color: "6A6A75", margin: 0,
  });

  s.addNotes(
    "Say the ID one out loud and explain the cost: no ID means renting leaves " +
    "nothing behind that could be used to find you. It hurts our conversion and " +
    "our fraud position. We did it anyway.\n\n" +
    "Anyone can claim to care about safety. Removing a field is a decision with " +
    "a price. About 45 seconds."
  );
}

/* ---------------------------------------------------------------- 7  demo */
{
  const s = pres.addSlide();
  s.background = dark;

  s.addText("Live demo", {
    x: 0.9, y: 2.6, w: 11.5, h: 1.1,
    fontFace: H, fontSize: 54, bold: true, color: Y, margin: 0,
  });
  s.addText("Scan → pay → collect → return.  Then the network behind it.", {
    x: 0.95, y: 3.8, w: 11.5, h: 0.5,
    fontFace: B, fontSize: 20, color: DIM, margin: 0,
  });

  s.addNotes(
    "Golden path only, about 2 minutes:\n\n" +
    "1. /kiosk — 11 banks, live\n" +
    "2. Two hours, R550 shown before committing\n" +
    "3. Use demo details — no ID asked for\n" +
    "4. Card — nowhere to type one, we only display the test number\n" +
    "5. Simulate payment, let the dispensing animation play\n" +
    "6. Receipt\n" +
    "7. /ai — move Eskom stage 0 to 4, forecast moves\n" +
    "8. Van route and what it cannot fix\n" +
    "9. Battery flagged to pull\n" +
    "10. Ask Juice: type an ID and card number, show what leaves the machine\n\n" +
    "If anything breaks: do not debug. Switch to the recording and keep talking."
  );
}

/* --------------------------------------------------------------- 8  close */
{
  const s = pres.addSlide();
  s.background = dark;
  s.addShape(pres.ShapeType.ellipse, { x: -2.0, y: 3.4, w: 6.8, h: 6.8, fill: { color: "1A1705" } });

  s.addText("Next", {
    x: 0.9, y: 0.9, w: 11.5, h: 0.7,
    fontFace: H, fontSize: 32, bold: true, color: WHITE, margin: 0,
  });

  const next = [
    "Swap synthetic telemetry for real cabinet check-ins.",
    "Connect a payment provider and an SMS gateway.",
    "Pilot at one taxi rank and one campus.",
  ];
  next.forEach((t, i) => {
    const y = 2.0 + i * 0.9;
    dot(s, 0.95, y + 0.1);
    s.addText(t, {
      x: 1.55, y, w: 10.5, h: 0.5,
      fontFace: B, fontSize: 20, color: WHITE, margin: 0,
    });
  });

  card(s, 0.9, 5.3, 11.5, 1.3, PANEL_2);
  s.addText("Pay for the time, share the power.", {
    x: 1.3, y: 5.65, w: 7, h: 0.6,
    fontFace: H, fontSize: 26, bold: true, color: Y, margin: 0,
  });
  s.addText("Thank you", {
    x: 8.4, y: 5.7, w: 3.6, h: 0.5,
    fontFace: H, fontSize: 24, bold: true, color: WHITE, align: "right", margin: 0,
  });

  s.addNotes(
    "State plainly, per rule 12: the AI models and the policy engine predate " +
    "this weekend. Built during the hackathon — the whole Python site and API, " +
    "the kiosk rental journey, the nearest-station finder, the safety page and " +
    "208 automated checks.\n\n" +
    "fleet.telemetry() is the single swap point for real data. Nothing " +
    "downstream changes.\n\n" +
    "Then the ask: what you would do with the prize. About 45 seconds."
  );
}

pres.writeFile({ fileName: "C:/dev/juicetech-hackathon/Juice-Tech-Pitch.pptx" })
  .then(f => console.log("wrote", f));
