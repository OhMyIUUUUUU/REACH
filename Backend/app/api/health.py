import time
from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import HealthResponse, APIInfoResponse

router = APIRouter()
start_time = time.time()

def get_uptime_str() -> str:
    elapsed_seconds = int(time.time() - start_time)
    hours, rem = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    if hours > 0:
        return f"{hours}h{minutes}m{seconds}s"
    elif minutes > 0:
        return f"{minutes}m{seconds}s"
    return f"{seconds}s"

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint"
)
def get_health() -> HealthResponse:
    """Returns the operational status, current UTC timestamp, and service uptime."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc),
        uptime=get_uptime_str()
    )

@router.get(
    "/info",
    response_model=APIInfoResponse,
    summary="Service metadata endpoint"
)
def get_info() -> APIInfoResponse:
    """Returns application name, version, running environment, and status."""
    return APIInfoResponse(
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        status="running"
    )
