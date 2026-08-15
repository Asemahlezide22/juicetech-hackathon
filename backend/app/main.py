"""Juice Tech API.

Run it from the backend/ folder with:
    uvicorn app.main:app --reload --port 8000

Interactive docs (great for demoing): http://localhost:8000/docs
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import config
from .database import create_db_and_tables, migrate
from .routers import ai, enquiries, kiosk, otp, pages, pricing, rentals, stations
from .seed import seed_if_empty

BACKEND_DIR = Path(__file__).resolve().parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    migrate()  # add columns to a database created by an older version
    seed_if_empty()
    yield


app = FastAPI(
    title="Juice Tech API",
    description="Power bank rentals, event charging and enquiries for Juice Tech.",
    version="1.0.0",
    lifespan=lifespan,
)

# The Vite dev server runs on a different port, so the browser needs CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSS, JavaScript and images for the HTML pages.
app.mount("/static", StaticFiles(directory=str(BACKEND_DIR / "static")), name="static")

app.include_router(pricing.router)
app.include_router(stations.router)
app.include_router(otp.router)
app.include_router(rentals.router)
app.include_router(enquiries.router)
app.include_router(ai.router)     # forecasting, battery health, concierge
app.include_router(kiosk.router)  # the hackathon kiosk demo
app.include_router(pages.router)  # HTML pages last, so /api/* wins any overlap


@app.get("/api/health", tags=["health"])
def health() -> dict:
    """Cheap liveness check."""
    return {"status": "ok", "service": "juicetech-api"}
