from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import RunCreate, RunResponse, MetricLog
from psycopg2.extras import Json
from typing import List

router = APIRouter()

@router.post("/{run_id}")
def log_metrics(run_id: int, log: MetricLog):
    """Log metrics for a specific run at a given step"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM runs WHERE id = %s", (run_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Run not found")

    cur.execute("""
        INSERT INTO metrics (run_id, step, metrics)
        VALUES (%s, %s, %s)
    """, (run_id, log.step, Json(log.metrics)))

    cur.execute("""
        UPDATE runs SET updated_at = CURRENT_TIMESTAMP WHERE id = %s
    """, (run_id,))

    conn.commit()
    conn.close()

    return {"success": True, "run_id": run_id, "step": log.step}