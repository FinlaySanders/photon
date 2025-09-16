from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_tables
from app.routers import runs, metrics
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Photon ML Tracker", lifespan=lifespan)

app.include_router(runs.router, prefix="/api/runs", tags=["runs"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",  # Sometimes localhost vs 127.0.0.1 matters
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/api/health")
def health():
    return {"status": "ok"}