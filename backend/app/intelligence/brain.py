"""JuiceBrain: the three models that make Juice Tech more than a vending machine.

  1. DemandForecaster  - how many banks each station needs in the next 24 hours
  2. HealthModel       - which individual batteries are about to fail
  3. rebalance()       - the van route that closes the gap between the two

A note on model choice, because judges ask. None of these are language models.
Gradient boosting on tabular telemetry is the correct tool for tabular
telemetry: it trains in under a second on a laptop, it runs offline in a venue
with no signal, and -- the part that matters for a company that has to answer
to an operations manager -- you can show exactly which feature drove the call.
The language model has one job in this product, further down in `agent.py`:
talking to humans.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_absolute_error, roc_auc_score

from . import fleet

DEMAND_FEATURES = ["hour", "dow", "is_weekend", "stage", "temp_c", "rain", "event", "slots"]
HEALTH_FEATURES = ["cycles", "capacity_pct", "resistance_mohm", "peak_temp_c",
                   "charge_faults", "swell_detected"]

# Charge one bank, and how much a station of each type earns from it, drive the
# rebalancing economics. R18 is the median basket at the pricing below.
REVENUE_PER_RENTAL = 18.0


class DemandForecaster:
    """Predicts hourly rentals per station.

    One model across every station, with station type one-hot encoded, rather
    than eighteen separate models. That is what lets a brand-new station start
    forecasting on day one instead of after two months of its own history --
    which is the difference between expanding into Delft and not bothering.
    """

    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=220, max_depth=4, learning_rate=0.08, random_state=fleet.SEED
        )
        self.columns: list[str] = []
        self.mae: float | None = None
        self.baseline_mae: float | None = None

    @staticmethod
    def _design(frame: pd.DataFrame) -> pd.DataFrame:
        x = frame[DEMAND_FEATURES].copy()
        # Hour is circular: 23:00 is one hour from 00:00, not twenty-three.
        x["hour_sin"] = np.sin(2 * np.pi * frame["hour"] / 24)
        x["hour_cos"] = np.cos(2 * np.pi * frame["hour"] / 24)
        return pd.concat([x, pd.get_dummies(frame["type"], prefix="type")], axis=1)

    def fit(self, history: pd.DataFrame) -> "DemandForecaster":
        """Train on everything but the last week, score on the week held out."""
        cutoff = history["ts"].max() - pd.Timedelta("7D")
        train, test = history[history["ts"] <= cutoff], history[history["ts"] > cutoff]

        x_train = self._design(train)
        self.columns = list(x_train.columns)
        self.model.fit(x_train, train["rentals"])

        predicted = self.model.predict(self._design(test)[self.columns])
        self.mae = float(mean_absolute_error(test["rentals"], predicted))

        # The honest yardstick: "same hour, same station, last week". Any
        # forecast that cannot beat that does not deserve to exist.
        naive = train.groupby(["station", "dow", "hour"])["rentals"].mean()
        guess = test.set_index(["station", "dow", "hour"]).index.map(naive)
        guess = pd.Series(guess, index=test.index).fillna(train["rentals"].mean())
        self.baseline_mae = float(mean_absolute_error(test["rentals"], guess))
        return self

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        design = self._design(frame).reindex(columns=self.columns, fill_value=0)
        return np.clip(self.model.predict(design), 0, None)

    def importances(self) -> pd.DataFrame:
        return (
            pd.DataFrame({"feature": self.columns, "importance": self.model.feature_importances_})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True)
        )

    def next_24h(self, history: pd.DataFrame, stage: int, rain: int,
                 event_stations: list[str] | None = None) -> pd.DataFrame:
        """Forecast the coming day under a scenario the ops team dials in.

        `stage` and `rain` are the two things an operator genuinely knows in
        advance -- Eskom publishes the schedule, the weather service publishes
        the front -- so they are inputs, not predictions.
        """
        event_stations = event_stations or []
        site = fleet.stations()
        start = history["ts"].max() + pd.Timedelta("1h")
        future = pd.date_range(start, periods=24, freq="h")

        recent_temp = history[history["ts"] > history["ts"].max() - pd.Timedelta("48h")]
        hourly_temp = recent_temp.groupby("hour")["temp_c"].mean()

        rows = []
        for _, s in site.iterrows():
            frame = pd.DataFrame({"ts": future})
            frame["hour"] = frame["ts"].dt.hour
            frame["dow"] = frame["ts"].dt.dayofweek
            frame["is_weekend"] = (frame["dow"] >= 5).astype(int)
            frame["stage"] = stage
            frame["temp_c"] = frame["hour"].map(hourly_temp).fillna(18.0)
            frame["rain"] = rain
            frame["event"] = int(s["station"] in event_stations)
            frame["slots"] = s["slots"]
            frame["type"] = s["type"]
            frame["station"] = s["station"]
            frame["station_id"] = s["station_id"]
            frame["forecast"] = self.predict(frame)
            rows.append(frame)

        return pd.concat(rows, ignore_index=True)


class HealthModel:
    """Flags the individual batteries that will fail within 30 days.

    This is the safety model. A lithium cell that swells or whose internal
    resistance runs away is a fire in a bag on a train, and no amount of good
    unit economics survives that photograph. It is also the environmental model:
    a cell pulled at the right moment is refurbishable, and a cell run to
    destruction is landfill.
    """

    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=180, max_depth=3, learning_rate=0.1, random_state=fleet.SEED
        )
        self.auc: float | None = None

    def fit(self, catalogue: pd.DataFrame) -> "HealthModel":
        split = int(len(catalogue) * 0.75)
        shuffled = catalogue.sample(frac=1, random_state=fleet.SEED)
        train, test = shuffled.iloc[:split], shuffled.iloc[split:]

        self.model.fit(train[HEALTH_FEATURES], train["failed_next_30d"])
        if test["failed_next_30d"].nunique() > 1:
            scores = self.model.predict_proba(test[HEALTH_FEATURES])[:, 1]
            self.auc = float(roc_auc_score(test["failed_next_30d"], scores))
        return self

    def score(self, catalogue: pd.DataFrame) -> pd.DataFrame:
        out = catalogue.copy()
        out["risk"] = self.model.predict_proba(catalogue[HEALTH_FEATURES])[:, 1]
        out["action"] = pd.cut(
            out["risk"],
            bins=[-0.01, 0.35, 0.65, 1.01],
            labels=["Keep in service", "Watch - service at next swap", "Pull now"],
        )
        return out.sort_values("risk", ascending=False)

    def importances(self) -> pd.DataFrame:
        return (
            pd.DataFrame({"signal": HEALTH_FEATURES, "importance": self.model.feature_importances_})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True)
        )


def rebalance(forecast: pd.DataFrame, stock: pd.DataFrame, van_capacity: int = 60) -> pd.DataFrame:
    """Decide which banks move where before the next peak.

    Deliberately not an optimiser. The exact version of this is a vehicle
    routing problem, which is NP-hard, and a driver in a bakkie at 05:00 needs
    an answer in one second, not a proof of optimality.

    Van capacity is split across the shortfall sites in proportion to how short
    each one is, then each drop is sourced from the deepest surplus. Proportional
    rather than strictly greedy, because a greedy split empties the whole van at
    the single worst site and leaves five others to run dry -- which is worse
    business and, more to the point, is not how a route works.
    """
    demand = forecast.groupby("station")["forecast"].sum().rename("demand_24h")
    peak = forecast.groupby("station")["forecast"].max().rename("peak_hour")
    board = stock.merge(demand, on="station").merge(peak, on="station")

    # Hold enough to cover the peak hour plus a quarter, capped by the cabinet.
    # Higher buffers look prudent on a slide and tie up capital in a cabinet
    # nobody is walking to.
    board["target"] = np.minimum(np.ceil(board["peak_hour"] * 1.25), board["slots"]).astype(int)
    board["gap"] = board["target"] - board["ready"]

    shortfall = board[board["gap"] > 0].sort_values("gap", ascending=False).copy()
    surplus = board[board["gap"] < 0].sort_values("gap").copy()
    surplus["spare"] = (-surplus["gap"]).astype(int)

    # Split the van proportionally to need before sourcing anything.
    total_need = shortfall["gap"].sum()
    if total_need > 0:
        share = shortfall["gap"] / total_need * van_capacity
        shortfall["allocation"] = np.minimum(shortfall["gap"], np.floor(share)).astype(int)
        # Floor above loses a few banks to rounding; hand them to the worst site.
        leftover = van_capacity - shortfall["allocation"].sum()
        for i in shortfall.index:
            if leftover <= 0:
                break
            room = int(shortfall.at[i, "gap"] - shortfall.at[i, "allocation"])
            add = int(min(room, leftover))
            shortfall.at[i, "allocation"] += add
            leftover -= add
    else:
        shortfall["allocation"] = 0

    moves, budget = [], van_capacity
    filled = {}
    for _, need in shortfall.iterrows():
        want = int(need["allocation"])
        for i, give in surplus.iterrows():
            if want <= 0 or budget <= 0:
                break
            take = int(min(want, give["spare"], budget))
            if take <= 0:
                continue
            moves.append({
                "from": give["station"],
                "to": need["station"],
                "banks": take,
                "closes_gap": f"{take}/{int(need['gap'])}",
                "revenue_unlocked": round(take * REVENUE_PER_RENTAL * 2.4, 0),
            })
            surplus.at[i, "spare"] -= take
            want -= take
            budget -= take
            filled[need["station"]] = filled.get(need["station"], 0) + take
        if budget <= 0:
            break

    # What the van cannot fix is not a routing problem, it is a capacity problem.
    # Surfacing it separately is how the same model tells us where to spend the
    # next R14 000 on a cabinet instead of another night of driving.
    board["moved_in"] = board["station"].map(filled).fillna(0).astype(int)
    board["unmet_gap"] = (board["gap"] - board["moved_in"]).clip(lower=0)

    return pd.DataFrame(moves), board


# A per-minute price_quote() lived here, left over from an earlier version of
# the product. Nothing called it, and it described a tariff this site does not
# charge, so it was a second source of truth waiting to contradict the first.
# Pricing now lives in exactly one place: app/config.py.
