from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import RunCreate, RunResponse
from psycopg2.extras import Json
from typing import List

router = APIRouter()

@router.get("/", response_model=List[RunResponse])
def get_runs(project: str = None):
    conn = get_db()
    cur = conn.cursor()

    if project:
        cur.execute("SELECT * FROM runs WHERE project = %s ORDER BY created_at DESC", (project,))
    else:
        cur.execute("SELECT * FROM runs ORDER BY created_at DESC")
    
    runs = cur.fetchall()
    conn.close()

    return runs

@router.post("/")
def create_run(run: RunCreate):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO runs (name, project)
        VALUES (%s, %s)
        ON CONFLICT (name, project) DO UPDATE SET updated_at = CURRENT_TIMESTAMP
        RETURNING id
    """, (run.name, run.project))

    run_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()

    return {"run_id": run_id}

@router.get("/{run_id}/metrics")
def get_run_metrics(run_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT step, metrics 
        FROM metrics 
        WHERE run_id = %s 
        ORDER BY step
    """, (run_id,))
    
    metrics = cur.fetchall()
    conn.close()

    return [{"step": row["step"], "metrics": row["metrics"]} for row in metrics]
