"""The Juice Tech fleet: stations, power banks, and the telemetry they emit.

Every number in here is generated from a fixed seed. That is deliberate. A demo
that reshuffles itself between rehearsal and the judges' table is a demo you
cannot rehearse. Same seed, same fleet, every single run.

In production this module is the only thing that changes: `stations()` reads the
station registry from Postgres and `telemetry()` reads the last 90 days of
cabinet check-ins instead of synthesising them. Everything downstream -- the
forecaster, the health model, the pricing engine -- keeps the same signature.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 2026
HOURS_OF_HISTORY = 24 * 60  # 60 days, enough to learn a weekly rhythm

# Station types behave very differently, so the model gets this as a feature.
#   event     - stadiums, festivals, conference venues. Spiky, schedule-driven.
#   transport - taxi ranks and train decks. Twin commuter peaks, very reliable.
#   campus    - universities. Term-time weekdays, dead on Sundays.
#   retail    - malls. Broad afternoon hump, busy Saturdays.
#   township  - spaza and community hubs. Steadiest demand, most load-shedding
#               sensitive, and the sites incumbents refuse to serve.
STATIONS = [
    # name,                        type,        lat,      lon,     cabinets, host
    ("Workshop 17 V&A Waterfront", "event",     -33.9068, 18.4183, 3, "Workshop 17"),
    ("Cape Town Stadium",          "event",     -33.9036, 18.4109, 6, "Stadium Ops"),
    ("Kirstenbosch Concerts",      "event",     -33.9881, 18.4324, 4, "SANBI Events"),
    ("Athlone Stadium",            "event",     -33.9603, 18.5122, 3, "City of CT"),
    ("Grand Parade Events",        "event",     -33.9258, 18.4232, 3, "City of CT"),
    ("CT Station Taxi Deck",       "transport", -33.9221, 18.4290, 8, "Golden Arrow"),
    ("Bellville Taxi Rank",        "transport", -33.9022, 18.6290, 6, "CODETA"),
    ("Langa Taxi Rank",            "transport", -33.9450, 18.5320, 4, "Langa Traders"),
    ("Mitchells Plain Terminus",   "transport", -34.0356, 18.6180, 5, "MP Taxi Assoc"),
    ("UCT Upper Campus",           "campus",    -33.9577, 18.4612, 5, "UCT SRC"),
    ("CPUT District Six",          "campus",    -33.9310, 18.4260, 4, "CPUT SRC"),
    ("Stellenbosch Neelsie",       "campus",    -33.9328, 18.8644, 4, "SU Student Union"),
    ("Canal Walk",                 "retail",    -33.8930, 18.5110, 5, "Hyprop"),
    ("Khayelitsha Mall",           "retail",    -34.0400, 18.6750, 5, "Khaya Traders"),
    ("Gugulethu Square",           "retail",    -33.9770, 18.5720, 4, "Gugs Square"),
    ("Nyanga Junction",            "township",  -33.9880, 18.5860, 4, "Nyanga Co-op"),
    ("Philippi Village",           "township",  -34.0100, 18.5820, 3, "Philippi Village"),
    ("Delft Community Hub",        "township",  -33.9700, 18.6480, 3, "Delft Youth Co-op"),
]

BANKS_PER_CABINET = 8

# Hour-of-day demand shape, 0..23, one curve per station type. These are the
# shapes an ops person would sketch on a napkin; the model learns the rest.
SHAPES = {
    "event":     [.05,.03,.02,.02,.02,.03,.05,.08,.12,.18,.28,.40,.52,.60,.68,.78,.88,1.0,.98,.92,.80,.60,.35,.15],
    "transport": [.04,.02,.02,.03,.10,.35,.72,1.0,.88,.55,.40,.38,.42,.45,.50,.62,.85,1.0,.82,.50,.28,.16,.10,.06],
    "campus":    [.03,.02,.02,.02,.03,.06,.14,.34,.62,.82,.92,.96,1.0,.94,.88,.80,.66,.48,.36,.30,.24,.16,.09,.05],
    "retail":    [.02,.01,.01,.01,.02,.04,.08,.16,.32,.54,.72,.86,.94,1.0,.98,.92,.84,.72,.58,.40,.22,.10,.05,.03],
    "township":  [.06,.04,.03,.03,.06,.16,.34,.52,.60,.64,.68,.72,.76,.78,.80,.86,.94,1.0,.96,.84,.66,.44,.24,.12],
}

# Weekday multiplier, Monday=0 .. Sunday=6.
WEEKDAY = {
    "event":     [.30,.32,.38,.50,.85,1.00,.72],
    "transport": [1.00,.98,.98,.96,1.00,.62,.34],
    "campus":    [1.00,1.00,.98,.96,.82,.30,.16],
    "retail":    [.62,.60,.64,.70,.88,1.00,.74],
    "township":  [.88,.86,.88,.90,1.00,.98,.72],
}

# Peak hourly rentals a fully stocked station of each type can pull. Kept below
# cabinet capacity so that a station running dry is a stocking failure we can
# fix with a van, not a physical limit we can only fix with more capex.
PEAK_RENTALS = {"event": 20, "transport": 16, "campus": 13, "retail": 12, "township": 9}


def stations() -> pd.DataFrame:
    """The station registry. One row per physical site."""
    frame = pd.DataFrame(
        STATIONS, columns=["station", "type", "lat", "lon", "cabinets", "host"]
    )
    frame["slots"] = frame["cabinets"] * BANKS_PER_CABINET
    frame["station_id"] = ["JT-%03d" % i for i in range(1, len(frame) + 1)]
    return frame


def loadshedding_schedule(index: pd.DatetimeIndex, rng: np.random.Generator) -> pd.Series:
    """Eskom stage, 0-6, per hour.

    Load shedding does not arrive hour by hour at random -- it arrives in blocks
    of a day or two at a stage, announced in advance. Modelling it as a daily
    block is what makes it forecastable, and being forecastable is the whole
    reason it belongs in the feature set.
    """
    days = pd.date_range(index[0].normalize(), index[-1].normalize(), freq="D")
    # Most days are clear. When it bites, it bites for a day at stage 2-6.
    daily = rng.choice([0, 0, 0, 0, 2, 2, 3, 4, 6], size=len(days))
    lookup = pd.Series(daily, index=days)
    return pd.Series(lookup.reindex(index.normalize()).to_numpy(), index=index)


def telemetry(hours: int = HOURS_OF_HISTORY) -> pd.DataFrame:
    """Hourly rental history for every station.

    Returns one row per (station, hour) with the features the forecaster trains
    on and the `rentals` target it learns to predict.
    """
    rng = np.random.default_rng(SEED)
    site = stations()

    end = pd.Timestamp("2026-08-15 08:00")  # hackathon morning
    index = pd.date_range(end=end, periods=hours, freq="h")

    stage = loadshedding_schedule(index, rng)

    # Cape Town winter: cold, wet, and people huddle indoors near the stations.
    day_of_year = index.dayofyear.to_numpy()
    temp = 17 + 6 * np.sin(2 * np.pi * (day_of_year - 20) / 365) \
             + 4 * np.sin(2 * np.pi * (index.hour.to_numpy() - 9) / 24) \
             + rng.normal(0, 1.5, len(index))
    rain = (rng.random(len(index)) < 0.18).astype(int)

    rows = []
    for _, s in site.iterrows():
        shape = np.array(SHAPES[s["type"]])
        weekday = np.array(WEEKDAY[s["type"]])
        peak = PEAK_RENTALS[s["type"]]

        # Each site has its own footfall multiplier -- a stadium is not a spaza.
        site_scale = rng.uniform(0.75, 1.25) * (s["cabinets"] / 4.0)

        # Event sites get scheduled surges: a concert, a match, a graduation.
        event_flag = np.zeros(len(index))
        if s["type"] in ("event", "campus"):
            n_events = max(1, int(len(index) / 24 / 7 * (2.2 if s["type"] == "event" else 0.9)))
            for _ in range(n_events):
                start = rng.integers(0, max(1, len(index) - 8))
                span = rng.integers(4, 9)
                event_flag[start:start + span] = 1

        base = peak * site_scale * shape[index.hour] * weekday[index.dayofweek]

        # The four levers that actually move demand in South Africa.
        base *= 1 + 0.22 * stage.to_numpy()          # no grid power, no home charging
        base *= 1 + 1.35 * event_flag                # a crowd is a demand spike
        base *= 1 + 0.16 * rain                      # rain keeps people inside, on phones
        base *= 1 + 0.012 * np.clip(temp - 24, 0, None)  # heat drains batteries

        rentals = rng.poisson(np.clip(base, 0.05, None))
        rentals = np.minimum(rentals, s["slots"])    # cannot rent what is not in the cabinet

        rows.append(pd.DataFrame({
            "ts": index,
            "station": s["station"],
            "station_id": s["station_id"],
            "type": s["type"],
            "slots": s["slots"],
            "stage": stage.to_numpy(),
            "temp_c": np.round(temp, 1),
            "rain": rain,
            "event": event_flag.astype(int),
            "rentals": rentals,
        }))

    frame = pd.concat(rows, ignore_index=True)
    frame["hour"] = frame["ts"].dt.hour
    frame["dow"] = frame["ts"].dt.dayofweek
    frame["is_weekend"] = (frame["dow"] >= 5).astype(int)
    return frame


def current_stock(history: pd.DataFrame) -> pd.DataFrame:
    """Where the banks physically are right now, and how charged they are.

    A station is only useful if it holds banks that are actually full, so the
    dashboard reports `ready` (>=80% charge), not raw stock.
    """
    rng = np.random.default_rng(SEED + 1)
    site = stations()

    # Sites that have been busy in the last day are the ones running dry.
    recent = history[history["ts"] > history["ts"].max() - pd.Timedelta("24h")]
    pressure = recent.groupby("station")["rentals"].sum()
    pressure = (pressure / pressure.max()).reindex(site["station"]).fillna(0.5).to_numpy()

    # Busy sites have drained overnight; quiet sites are sitting on stock nobody
    # wants. That mismatch -- not a fleet-wide shortage -- is what the van fixes.
    fill = np.clip(rng.uniform(0.70, 1.00, len(site)) - 0.62 * pressure, 0.05, 1.0)
    stock = np.round(site["slots"].to_numpy() * fill).astype(int)
    ready = np.round(stock * rng.uniform(0.80, 0.98, len(site))).astype(int)

    site = site.copy()
    site["stock"] = stock
    site["ready"] = ready
    site["out_with_users"] = site["slots"] - site["stock"]
    site["fill_pct"] = (site["stock"] / site["slots"] * 100).round(0)
    return site


def banks(history: pd.DataFrame) -> pd.DataFrame:
    """Per-battery service record: the input to the health model.

    Every bank carries a cycle count, a measured internal resistance, the
    capacity it can still hold versus its nameplate, and how hot it runs. Those
    four numbers are what a battery management system actually reports, and
    they are what predicts a cell going bad.
    """
    rng = np.random.default_rng(SEED + 2)
    site = stations()
    total = int(site["slots"].sum())

    station_of = np.repeat(site["station"].to_numpy(), site["slots"].to_numpy())
    type_of = np.repeat(site["type"].to_numpy(), site["slots"].to_numpy())

    # Fleet bought in waves, so age is lumpy rather than uniform.
    age_days = rng.choice([40, 120, 240, 420, 600], size=total, p=[.22, .26, .24, .18, .10])
    age_days = age_days + rng.integers(-25, 25, total)
    cycles = np.clip((age_days * rng.uniform(0.55, 1.15, total)).astype(int), 5, None)

    # Capacity fades with cycles; heat accelerates it. 500 cycles is the point
    # where a decent 20 000 mAh cell is down around 80% of nameplate.
    heat = rng.normal(31, 4.5, total) + np.where(type_of == "event", 2.5, 0)
    fade = 1 - (cycles / 1400) * rng.uniform(0.75, 1.25, total) - np.clip(heat - 33, 0, None) * 0.006
    capacity_pct = np.clip(fade * 100, 32, 100)

    # Internal resistance is the early-warning signal: it climbs before capacity
    # collapses and before a cell ever gets hot enough to be dangerous.
    resistance = 45 + (cycles / 1400) * 55 + np.clip(heat - 30, 0, None) * 1.8 \
                 + rng.normal(0, 6, total)

    charge_faults = rng.poisson(np.clip((cycles / 900) * 1.4, 0.02, None))
    swell = ((resistance > 95) & (rng.random(total) < 0.45)).astype(int)

    frame = pd.DataFrame({
        "bank_id": ["PB-%05d" % i for i in range(1, total + 1)],
        "station": station_of,
        "type": type_of,
        "cycles": cycles,
        "age_days": age_days,
        "capacity_pct": capacity_pct.round(1),
        "resistance_mohm": resistance.round(1),
        "peak_temp_c": heat.round(1),
        "charge_faults": charge_faults,
        "swell_detected": swell,
    })

    # Ground truth for training: a bank "fails in the next 30 days" when the
    # physics says it is already on the way out. Real deployments label this
    # from warranty returns instead.
    risk = (
        0.9 * (frame["resistance_mohm"] > 92)
        + 0.7 * (frame["capacity_pct"] < 62)
        + 0.8 * frame["swell_detected"]
        + 0.4 * (frame["charge_faults"] >= 3)
        + 0.3 * (frame["peak_temp_c"] > 38)
    )
    # Some noise, because real batteries fail for reasons no sensor saw coming and
    # a model that scores a perfect AUC is a model that has been handed the answer.
    noise = rng.normal(0, 0.30, total)
    frame["failed_next_30d"] = ((risk + noise) > 0.62).astype(int)
    return frame
