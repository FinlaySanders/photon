import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import psycopg2
from psycopg2.extras import Json

class RunCreate(BaseModel):
    name: str
    project: str = "default"

class MetricLog(BaseModel):
    metrics: Dict[str, Any]
    step: int

def get_db():
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://photon:photon@db:5432/photon")
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

def create_tables():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            project VARCHAR(255) DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, project)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            run_id INTEGER REFERENCES runs(id) ON DELETE CASCADE,
            step INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metrics JSONB
        )
    """)
    
    conn.commit()
    conn.close()
    print("Tables created")

# endpoints
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/runs")
def start_run(run: RunCreate):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO runs (name, project)
        VALUES (%s, %s)
        ON CONFLICT (name, project) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
    """, (run.name, run.project))
    
    run_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    
    return {"run_id": run_id}

@app.post("/runs/{run_id}/log")
def log_metrics(run_id: int, log: MetricLog):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO metrics (run_id, step, metrics)
        VALUES (%s, %s, %s)
    """, (run_id, log.step, Json(log.metrics)))
    
    conn.commit()
    conn.close()
    
    return {"success": True}