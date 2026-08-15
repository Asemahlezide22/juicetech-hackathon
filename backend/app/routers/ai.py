"""The AI layer: demand forecasting, battery health, rebalancing and the
customer concierge.

Two deliberate choices worth knowing before reading further:

  The forecasting and health models are gradient boosting, not language
  models. Tabular telemetry is what gradient boosting is for: it trains in
  seconds on a laptop, runs with no internet, and reports which feature drove
  each call. The language model has one job — talking to humans.

  Every customer message is redacted before it leaves this machine. That runs
  first and unconditionally, so an ID or card number never reaches a third
  party even if the model call itself fails.

Training is lazy: nothing is built until the first AI request, so the site
still starts instantly.
"""

from pathlib import Path

from fastapi import APIRouter, Body, Query, Request
from fastapi.templating import Jinja2Templates

from .. import content
from ..intelligence import fleet, llm, service

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BACKEND_DIR / "templates"))

router = APIRouter(tags=["ai"])


# ------------------------------------------------------------------- JSON API

@router.get("/api/ai/status")
def ai_status() -> dict:
    """Model scorecard. Cheap to call once the models are warm."""
    state = service.warm()
    forecaster, health = state["forecaster"], state["health"]

    return {
        "demand_model": {
            "kind": "GradientBoostingRegressor",
            "mae": round(forecaster.mae, 3),
            "baseline_mae": round(forecaster.baseline_mae, 3),
            "improvement_pct": round((1 - forecaster.mae / forecaster.baseline_mae) * 100, 1),
            "rows_trained": int(len(state["history"])),
            "top_features": forecaster.importances().head(5).to_dict(orient="records"),
        },
        "health_model": {
            "kind": "GradientBoostingClassifier",
            "auc": round(health.auc, 3) if health.auc else None,
            "banks_scored": int(len(state["catalogue"])),
            "top_signals": health.importances().head(5).to_dict(orient="records"),
        },
        "policy_index": state["policy_index"] is not None,
        "language_model": llm.provider_status(),
    }


@router.get("/api/ai/forecast")
def ai_forecast(
    stage: int = Query(0, ge=0, le=6, description="Eskom load shedding stage"),
    rain: int = Query(0, ge=0, le=1),
) -> dict:
    """24-hour demand per station under a scenario the operator dials in."""
    return service.forecast(stage=stage, rain=rain)


@router.get("/api/ai/rebalance")
def ai_rebalance(
    stage: int = Query(0, ge=0, le=6),
    rain: int = Query(0, ge=0, le=1),
    van: int = Query(60, ge=1, le=500),
) -> dict:
    """Tonight's van run, and the shortfall a van cannot fix."""
    return service.rebalance(stage=stage, rain=rain, van=van)


@router.get("/api/ai/health")
def ai_health(limit: int = Query(25, ge=1, le=200)) -> dict:
    """Which individual batteries are heading for failure."""
    return service.health(limit=limit)


@router.get("/api/ai/impact")
def ai_impact() -> dict:
    """Unit economics and the environmental model."""
    return service.impact_report()


@router.post("/api/ai/chat")
def ai_chat(payload: dict = Body(...)) -> dict:
    """Answer a customer question, grounded in our published policies.

    The message is redacted before it is sent anywhere. The response reports
    what was stripped, so the redaction is visible rather than a claim.
    """
    message = str(payload.get("message", ""))[:1000]
    language = str(payload.get("language", "English"))
    return service.chat(message, language)


@router.get("/api/ai/ops-brief")
def ai_ops_brief(stage: int = Query(0, ge=0, le=6), rain: int = Query(0, ge=0, le=1)) -> dict:
    """The four-sentence brief a depot manager reads before loading the van."""
    return {"brief": service.ops_brief(stage=stage, rain=rain)}


# ------------------------------------------------------------------ HTML page

@router.get("/ai", include_in_schema=False)
def ai_page(
    request: Request,
    stage: int = Query(0, ge=0, le=6),
    rain: int = Query(0, ge=0, le=1),
):
    """Operations view: what the models predict and what to do about it."""
    state = service.warm()
    forecast = service.forecast(stage=stage, rain=rain)
    rebalance = service.rebalance(stage=stage, rain=rain)
    health = service.health(limit=8)

    # Network-wide hourly totals, for the chart.
    hours = sorted({p["hour"] for pts in forecast["stations"].values() for p in pts})
    totals = []
    for hour in hours:
        total = sum(
            p["value"] for pts in forecast["stations"].values()
            for p in pts if p["hour"] == hour
        )
        totals.append({"hour": hour, "value": round(total, 1)})

    busiest = sorted(forecast["totals"].items(), key=lambda kv: kv[1], reverse=True)[:6]

    return templates.TemplateResponse(
        request=request,
        name="ai.html",
        context={
            "brand": content.BRAND,
            "nav": content.NAV,
            "current_url": request.url.path,
            "stage": stage,
            "rain": rain,
            "model": forecast["model"],
            "health": health,
            "rebalance": rebalance,
            "totals": totals,
            "peak": max((t["value"] for t in totals), default=1) or 1,
            "busiest": busiest,
            "stations_count": len(fleet.stations()),
            "banks_count": int(len(state["catalogue"])),
            "llm_status": llm.provider_status(),
        },
    )
