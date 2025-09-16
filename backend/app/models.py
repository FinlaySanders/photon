from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class RunCreate(BaseModel):
    name: str
    project: str = "default"

class RunResponse(BaseModel):
    id: int
    name: str
    project: str
    status: str
    created_at: datetime
    updated_at: datetime

class MetricLog(BaseModel):
    metrics: Dict[str, Any]
    step: int

class MetricResponse(BaseModel):
    step: int
    metrics: Dict[str, Any]
    timestamp: datetime
