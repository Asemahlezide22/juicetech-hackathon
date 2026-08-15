"""The language-model half of Juice Tech: the parts that talk to people.

Two jobs, and only two:

  ops_briefing()  turns the forecaster's numbers into the four sentences a
                  depot manager reads at 05:00 before loading the bakkie.
  concierge()     answers a customer over WhatsApp or USSD, in their language,
                  grounded in our own published policy documents.

Everything here degrades rather than crashes. A hackathon venue's wifi will fail
at the worst possible moment, and a demo that dies with a stack trace in front of
a judge is a lost demo. If the model is unreachable, `_safe()` returns a written
fallback and the app carries on.
"""

from __future__ import annotations

import pandas as pd

from . import llm
from . import retrieve

# Pricing is read from the single source of truth rather than restated here.
# The assistant previously quoted a per-minute tariff the site never charged,
# which is exactly the drift this import prevents.
from ..config import (
    DEPOSIT,
    GRACE_MINUTES,
    LATE_FEE_PER_30,
    PACKAGES,
    REPLACEMENT_FEE,
)

_ONE_HOUR = PACKAGES["1h"]["price"]
_TWO_HOUR = PACKAGES["2h"]["price"]

LANGUAGES = {
    "English": "English",
    "isiXhosa": "isiXhosa",
    "Afrikaans": "Afrikaans",
    "isiZulu": "isiZulu",
    "Sesotho": "Sesotho",
}

# The rules the customer-facing agent may never break. These are product policy,
# not decoration: each one maps to a promise we make on the cabinet itself.
CONCIERGE_RULES = f"""
You are Juice, the assistant for Juice Tech, a South African shared power bank
network. Slogan: "Pay for the time, share the time."

HARD RULES
- Never ask for, accept, or repeat a card number, CVV, PIN, ID number, or password.
  If a customer offers one, tell them to stop and that we never need it.
- Never claim to know where a customer is. We track batteries, not people.
- Pricing: R{_ONE_HOUR} for one hour, R{_TWO_HOUR} for two hours, plus a
  refundable R{DEPOSIT} deposit released when the bank is returned.
  {GRACE_MINUTES} minutes grace after the time is up, then R{LATE_FEE_PER_30}
  per additional 30 minutes, capped at the R{REPLACEMENT_FEE} replacement value.
  Prices never rise during load shedding.
- Our cables carry power only. The data pins are physically absent, so nothing
  can read or write to a customer's phone. Say this plainly if asked about safety.
- If you do not know something, say so and offer to hand over to a human on
  WhatsApp. Do not invent station names, prices, or policies.
- Keep replies under 60 words. Many customers pay for every kilobyte and read
  this on a feature phone.
"""

FALLBACK_CONCIERGE = (
    f"I can't reach the network right now, so here's the short version: "
    f"R{_ONE_HOUR} for an hour, R{_TWO_HOUR} for two, plus a refundable "
    f"R{DEPOSIT} deposit you get back on return. Return the bank to any Juice "
    f"Tech cabinet with a free slot. Our cables carry power only, so nothing can "
    f"touch your phone's data. Reply HELP to reach a human."
)

FALLBACK_BRIEFING = (
    "Offline mode: the forecast table and the move list on this screen are still "
    "live -- they run on the local model, not the internet. Load the van from the "
    "surplus column and drop at the shortfall column, biggest gap first."
)


def _safe(system: str, user: str, fallback: str, max_tokens: int = 700) -> str:
    """Ask the model, but never let a network failure take the demo down."""
    try:
        reply = llm.ask(system, user, max_tokens=max_tokens)
        return reply.strip() if reply and reply.strip() else fallback
    except Exception as exc:  # noqa: BLE001 - any failure means fall back, loudly but safely
        return f"{fallback}\n\n_(model unreachable: {type(exc).__name__})_"


def ops_briefing(board: pd.DataFrame, moves: pd.DataFrame, stage: int,
                 rain: int, events: list[str]) -> str:
    """Natural-language shift brief for the depot manager."""
    summary = board[["station", "type", "ready", "target", "gap", "demand_24h"]] \
        .sort_values("gap", ascending=False).head(8).to_string(index=False)
    move_text = moves.to_string(index=False) if len(moves) else "No moves required."

    return _safe(
        system=(
            "You write the morning shift brief for the operations manager of a "
            "power bank network in Cape Town. Four sentences maximum. Lead with "
            "the single site most at risk of running dry. Name real numbers from "
            "the tables. Plain English, no jargon, no bullet points, no preamble."
        ),
        user=(
            f"Eskom stage today: {stage}. Rain forecast: {'yes' if rain else 'no'}. "
            f"Events on: {', '.join(events) if events else 'none'}.\n\n"
            f"STATION BOARD (gap = banks short of target):\n{summary}\n\n"
            f"PLANNED MOVES:\n{move_text}"
        ),
        fallback=FALLBACK_BRIEFING,
        max_tokens=400,
    )


def health_note(flagged: pd.DataFrame) -> str:
    """One paragraph on what the battery health model found, for the safety log."""
    if not len(flagged):
        return "No batteries currently meet the pull threshold. Fleet is clear."

    table = flagged.head(10)[
        ["bank_id", "station", "cycles", "capacity_pct", "resistance_mohm",
         "swell_detected", "risk"]
    ].to_string(index=False)

    return _safe(
        system=(
            "You are the safety officer for a shared battery fleet. In three "
            "sentences, state how many units must be pulled, the dominant "
            "failure signal across them, and what happens to the cells after "
            "they are pulled. Factual, calm, no alarm language."
        ),
        user=f"{len(flagged)} units flagged. Top offenders:\n{table}",
        fallback=(
            f"{len(flagged)} units are above the pull threshold, mostly on rising "
            "internal resistance. They are removed at the next swap, tested at the "
            "depot, and either refurbished or sent to a licensed e-waste recycler."
        ),
        max_tokens=300,
    )


def concierge(question: str, language: str = "English",
              index: retrieve.Index | None = None) -> tuple[str, list[str]]:
    """Answer a customer. Returns the reply and the policy passages it leaned on.

    When a policy index is loaded, the answer is grounded in our own published
    documents -- the terms, the privacy notice, the safety sheet. That is what
    stops the assistant from inventing a refund policy we never agreed to.
    """
    passages: list[str] = []
    context = ""
    if index is not None:
        passages = index.search(question, top_k=4)
        if passages:
            context = "\n\n---\n\n".join(passages)

    grounding = (
        f"\n\nOUR PUBLISHED POLICY (answer from this where it applies):\n{context}"
        if context else
        "\n\nNo policy document loaded. Answer only from the hard rules above."
    )

    # Generous token budget despite the 60-word limit in the rules: current
    # Gemini and Groq models spend tokens on internal reasoning before they
    # write, and a tight cap truncates the answer mid-sentence. Non-Latin
    # scripts also tokenise far less efficiently than English, so an isiXhosa
    # reply of the same length costs noticeably more.
    reply = _safe(
        system=CONCIERGE_RULES + grounding + f"\n\nReply in {language}.",
        user=question,
        fallback=FALLBACK_CONCIERGE,
        max_tokens=1500,
    )
    return reply, passages


def redact(text: str) -> tuple[str, list[str]]:
    """Strip anything that looks like personal data before it reaches the model.

    This runs on every customer message on its way out of the handset. It is
    crude on purpose -- a regex that is too clever fails open, and failing open
    with someone's ID number is the failure that ends a company. Anything that
    even resembles an SA ID, a card, or an account number is destroyed at the
    edge, before it is ever transmitted.
    """
    import re

    patterns = [
        (r"\b\d{13}\b", "[SA-ID-REMOVED]"),                       # SA ID number
        (r"\b\d(?:[ -]?\d){12,18}\b", "[CARD-REMOVED]"),          # card PAN
        # CVV written either way round. The label-first form ("cvv 123") is by
        # far the common one and was previously missed, because the original
        # pattern only looked for digits *followed* by the label.
        (r"(?i)\b(?:cvv|cvc)\b\s*[:=]?\s*\d{3,4}\b", "[CVV-REMOVED]"),
        (r"(?i)\b\d{3,4}\b(?=\s*(?:cvv|cvc)\b)", "[CVV-REMOVED]"),
        # "my pin is 4821" used to leave the digits behind: the trailing \w+
        # matched the word "is" and stopped. Allow the filler word explicitly so
        # the secret itself is what gets destroyed.
        (r"(?i)\b(?:pin|passcode|password)\b\s*(?:is|=|:)?\s*\S+", "[SECRET-REMOVED]"),
        (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "[EMAIL-REMOVED]"),
    ]

    found = []
    cleaned = text
    for pattern, label in patterns:
        cleaned, hits = re.subn(pattern, label, cleaned)
        if hits:
            found.append(label.strip("[]"))
    return cleaned, found
