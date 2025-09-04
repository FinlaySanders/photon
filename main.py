import requests
import random
import time
import os

class PhotonClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("PHOTON_API_URL", "http://localhost:8000")
        self.current_run_id = None
    
    def create_run(self, name, project="default"):
        response = requests.post(
            f"{self.base_url}/runs",
            json={"name": name, "project": project}
        )
        response.raise_for_status()
        self.current_run_id = response.json()["run_id"]
        return self.current_run_id
    
    def log(self, metrics, step, run_id=None):
        run_id = run_id or self.current_run_id
        if not run_id:
            raise ValueError("No run_id. Call create_run() first")
        
        response = requests.post(
            f"{self.base_url}/runs/{run_id}/log",
            json={"metrics": metrics, "step": step}
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    client = PhotonClient()
    
    run_id = client.create_run("my_experiment", "test")
    print(f"Started run with ID: {run_id}")
    
    for step in range(10):
        metrics = {
            "loss": random.random(),
            "accuracy": random.random(),
        }
        
        client.log(metrics, step)
        
        print(f"Step {step}: loss={metrics['loss']:.3f}, accuracy={metrics['accuracy']:.3f}")
        time.sleep(0.1)
    
    print("Done")