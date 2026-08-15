"""Pricing endpoint.

The website reads its prices from here so the site and the stations can never
show different numbers.
"""

from fastapi import APIRouter

from .. import config

router = APIRouter(prefix="/api/pricing", tags=["pricing"])


@router.get("")
def get_pricing() -> dict:
    """Everything the UI needs to display prices and explain the fees."""
    return {
        "currency": "ZAR",
        "packages": list(config.PACKAGES.values()),
        "deposit": config.DEPOSIT,
        "replacement_fee": config.REPLACEMENT_FEE,
        "grace_minutes": config.GRACE_MINUTES,
        "late_fee_per_30": config.LATE_FEE_PER_30,
    }
