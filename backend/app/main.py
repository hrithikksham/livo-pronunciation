from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.routers.analyze import router as analyze_router
from app.routers.health import router as health_router

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.
    """

    logger.info("Starting Pronunciation Scorer Backend")

    yield

    logger.info("Shutting down Pronunciation Scorer Backend")


app = FastAPI(
    title="Pronunciation Scoring API",
    description="AI-powered pronunciation analysis using Whisper + LLM",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

###########################################################################
# Middleware
###########################################################################

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###########################################################################
# Exception Handlers
###########################################################################

register_exception_handlers(app)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    analyze_router,
    prefix="/api/v1",
    tags=["Analysis"],
)

@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse(
        status_code=200,
        content={
            "service": "Pronunciation Scoring API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
        },
    )