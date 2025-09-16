import os
import requests
from datetime import datetime

API_URL = os.getenv("PHOTON_API_URL", "http://localhost:8000/api")

_run = None

def init(name=None, project=None):
    global _run

    project = project or os.getenv("PHOTON_PROJECT", "default")
    name = name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        r = requests.post(
            f"{API_URL}/runs", 
            json={"name": name, "project": project},
            timeout=3
        )
        _run = {"id": r.json()["run_id"], "step": 0}
        print(f"Photon: Started run {_run['id']}")

    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to Photon at {API_URL}")
        _run = None
    except Exception as e:
        print(f"Error: {e}")
        _run = None

def log(step=None, **metrics):
    global _run

    if _run is None:
        init()

    if _run is None:
        return

    if step is None:
        step = _run["step"]
        _run["step"] += 1

    try:
        requests.post(
            f"{API_URL}/metrics/{_run['id']}",
            json={"step": step, "metrics": metrics},
            timeout=1
        )
    except:
        pass