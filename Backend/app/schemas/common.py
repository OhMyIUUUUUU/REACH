from datetime import datetime
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    uptime: str

class APIInfoResponse(BaseModel):
    name: str
    version: str
    environment: str
    status: str
