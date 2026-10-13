import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.router import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database tables are created if not initialized by migrations
    try:
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.warning("Could not auto-create tables (PostgreSQL may be starting or offline): %s", e)
    yield
    logger.info("Shutting down REACH Python backend...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Python FastAPI REST backend for REACH platform featuring PostgreSQL ORM, JWT Authentication, and Scikit-Learn/NLTK Reviewer Matching.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include central API router (/api/health, /api/auth, /api/nlp)
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to REACH Backend API",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "info": "/api/info",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting REACH FastAPI backend on http://%s:%d", settings.HOST, settings.PORT)
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
