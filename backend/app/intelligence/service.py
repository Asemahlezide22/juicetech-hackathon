"""The layer between Flask and the models.

Everything expensive -- generating 60 days of telemetry, training the forecaster,
training the health classifier, indexing the policy documents -- happens once, on
first use, and is then held in module state. Flask serves a request in
milliseconds afterwards.

Nothing in here knows about HTTP, and nothing in `app.py` knows about pandas.
That boundary is what lets the whole backend be tested from a plain Python shell,
and it is the honest answer to "how would you put this in production": you would
swap `fleet.telemetry()` for a database read and leave this file alone.
"""

from __future__ import annotations

import threading
from pathlib import Path

from . import agent, brain, fleet, impact, ingest, retrieve

_lock = threading.Lock()
_state: dict = {}


def warm() -> dict:
    """Build everything once. Safe to call from several requests at once."""
    if "ready" in _state:
        return _state

    with _lock:
        if "ready" in _state:               # another thread won the race
            return _state

        history = fleet.telemetry()
        catalogue = fleet.banks(history)

        _state.update(
            history=history,
            catalogue=catalogue,
            forecaster=brain.DemandForecaster().fit(history),
            health=brain.HealthModel().fit(catalogue),
            policy_index=_policy_index(),
            ready=True,
        )
    return _state


def _policy_index() -> retrieve.Index | None:
    chunks: list[str] = []
    folder = Path(__file__).resolve().parent.parent / "policies"
    for path in sorted(folder.glob("*")):
        if path.suffix.lower() in {".md", ".txt", ".pdf", ".docx"}:
            chunks.extend(ingest.chunk(ingest.read_file(path.name, path.read_bytes())))
    return retrieve.Index(chunks) if chunks else None


def policy_index() -> retrieve.Index | None:
    """The policy index on its own, without training any models.

    The chat widget only needs the documents to ground its answers. Calling
    warm() for that would generate 60 days of telemetry and fit two gradient
    boosting models first — several seconds a customer should not wait for
    before their first reply.
    """
    if "policy_index" in _state:
        return _state["policy_index"]

    with _lock:
        if "policy_index" not in _state:
            _state["policy_index"] = _policy_index()

    return _state["policy_index"]


# --------------------------------------------------------------------- stations

def stations() -> list[dict]:
    """Every station with its live stock, ready for JSON."""
    state = warm()
    stock = fleet.current_stock(state["history"])
    return stock.to_dict(orient="records")


def station_names() -> list[str]:
    return fleet.stations()["station"].tolist()


# --------------------------------------------------------------------- forecast

def forecast(stage: int = 0, rain: int = 0, events: list[str] | None = None) -> dict:
    """24-hour demand forecast for every station, plus the model's own scorecard.

    `stage` and `rain` are inputs rather than predictions because an operator
    genuinely knows both a day ahead -- Eskom publishes the schedule and the
    weather service publishes the front.
    """
    state = warm()
    frame = state["forecaster"].next_24h(
        state["history"], stage=stage, rain=rain, event_stations=events or [])

    per_station: dict[str, list[dict]] = {}
    for station, group in frame.groupby("station"):
        per_station[station] = [
            {"hour": ts.strftime("%H:%M"), "value": round(float(v), 2)}
            for ts, v in zip(group["ts"], group["forecast"])
        ]

    model = state["forecaster"]
    return {
        "stations": per_station,
        "totals": {s: round(float(sum(p["value"] for p in pts)), 1)
                   for s, pts in per_station.items()},
        "peaks": {s: round(max(p["value"] for p in pts), 1)
                  for s, pts in per_station.items()},
        "model": {
            "mae": round(model.mae, 3),
            "baseline_mae": round(model.baseline_mae, 3),
            "lift_pct": round((1 - model.mae / model.baseline_mae) * 100, 1),
            "rows_trained": int(len(state["history"])),
            "features": model.importances().head(8).to_dict(orient="records"),
        },
        "scenario": {"stage": stage, "rain": rain, "events": events or []},
    }


def rebalance(stage: int = 0, rain: int = 0, events: list[str] | None = None,
              van: int = 60) -> dict:
    """Tonight's van run, and the shortfall the van cannot fix."""
    state = warm()
    frame = state["forecaster"].next_24h(
        state["history"], stage=stage, rain=rain, event_stations=events or [])
    stock = fleet.current_stock(state["history"])
    moves, board = brain.rebalance(frame, stock, van_capacity=van)

    columns = ["station", "type", "ready", "target", "gap", "moved_in",
               "unmet_gap", "demand_24h", "peak_hour"]
    board_out = board[columns].round(1).sort_values("gap", ascending=False)

    unmet = board[board["unmet_gap"] > 0].nlargest(5, "unmet_gap")

    return {
        "moves": moves.to_dict(orient="records") if len(moves) else [],
        "banks_moved": int(moves["banks"].sum()) if len(moves) else 0,
        "revenue_unlocked": float(moves["revenue_unlocked"].sum()) if len(moves) else 0.0,
        "board": board_out.to_dict(orient="records"),
        "unmet_total": int(board["unmet_gap"].sum()),
        # The banks the van cannot cover are not a routing failure, they are a
        # capacity signal: this is the same model saying where the next cabinet goes.
        "expansion": [{"station": r.station, "short": int(r.unmet_gap)}
                      for r in unmet.itertuples()],
    }


# ----------------------------------------------------------------------- health

def health(limit: int = 25) -> dict:
    state = warm()
    model = state["health"]
    scored = model.score(state["catalogue"])

    columns = ["bank_id", "station", "cycles", "capacity_pct", "resistance_mohm",
               "peak_temp_c", "charge_faults", "swell_detected", "risk", "action"]
    top = scored.head(limit)[columns].copy()
    top["risk"] = top["risk"].round(3)
    top["action"] = top["action"].astype(str)

    counts = scored["action"].value_counts()
    return {
        "units": top.to_dict(orient="records"),
        "scored": int(len(scored)),
        "pull_now": int(counts.get("Pull now", 0)),
        "watch": int(counts.get("Watch - service at next swap", 0)),
        "keep": int(counts.get("Keep in service", 0)),
        "auc": round(model.auc, 3) if model.auc else None,
        "signals": model.importances().to_dict(orient="records"),
        "refurb_rate": impact.ASSUMPTIONS["refurb_rate"],
    }


# ----------------------------------------------------------------------- impact

def impact_report(overrides: dict | None = None) -> dict:
    state = warm()
    stock = fleet.current_stock(state["history"])
    banks_in_fleet = int(stock["slots"].sum())

    assumptions = dict(impact.ASSUMPTIONS)
    for key, value in (overrides or {}).items():
        if key in assumptions:
            try:
                assumptions[key] = float(value)
            except (TypeError, ValueError):
                pass

    return {
        "fleet": {"banks": banks_in_fleet, "stations": int(len(stock))},
        "economics": impact.economics(banks_in_fleet, len(stock), assumptions),
        "environment": impact.environment(banks_in_fleet, assumptions),
        "assumptions": assumptions,
    }


def buy_vs_rent(events: int, hours: int) -> dict:
    return impact.buy_vs_rent(events, hours)


# -------------------------------------------------------------------- concierge

def chat(message: str, language: str = "English") -> dict:
    """Answer a customer, but strip anything personal before it leaves the box.

    The redaction runs first and unconditionally. A regex that is too clever
    fails open, and failing open with somebody's ID number is the failure that
    ends a company -- so anything that even resembles one is destroyed here.
    """
    cleaned, stripped = agent.redact(message)
    # policy_index() rather than warm(): the concierge needs the documents,
    # not the forecasting and battery models.
    reply, passages = agent.concierge(cleaned, language, policy_index())
    return {
        "reply": reply,
        "redacted": stripped,
        "sent_to_model": cleaned,
        "sources": [p[:400] for p in passages],
    }


def ops_brief(stage: int = 0, rain: int = 0, events: list[str] | None = None,
              van: int = 60) -> str:
    state = warm()
    frame = state["forecaster"].next_24h(
        state["history"], stage=stage, rain=rain, event_stations=events or [])
    stock = fleet.current_stock(state["history"])
    moves, board = brain.rebalance(frame, stock, van_capacity=van)
    return agent.ops_briefing(board, moves, stage, rain, events or [])
