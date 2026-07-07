
from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get(
    "/health",
    summary="Application Health Check",
    response_description="Application health status",
)
async def health_check():
    """
    Returns application health information.
    """

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dependencies": {
            "groq": "configured" if settings.GROQ_API_KEY else "missing",
            "openai": (
                "configured"
                if settings.OPENAI_API_KEY
                else "not_configured"
            ),
        },
    }


@router.get(
    "/ready",
    summary="Readiness Probe",
)
async def readiness_probe():
    """
    Indicates whether the application is ready
    to receive traffic.
    """

    return {
        "ready": True,
    }


@router.get(
    "/live",
    summary="Liveness Probe",
)
async def liveness_probe():
    """
    Indicates whether the application is alive.
    """

    return {
        "alive": True,
    }