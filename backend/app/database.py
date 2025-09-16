import os
import psycopg2
from psycopg2.extras import Json, RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://photon:photon@localhost:5432/photon")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def create_tables():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            project VARCHAR(255) DEFAULT 'default',
            status VARCHAR(50) DEFAULT 'running',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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