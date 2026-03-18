"""Main FastAPI application for My Project Name."""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

# Load environment variables from .env file FIRST
load_dotenv()

# Configure logging AFTER loading .env
from my_app.core.logger import configure_root_logging
configure_root_logging()

from my_app.core.auth import verify_bearer_token
from my_app.core.config import AppConfig, UvicornConfig
from my_app.core.graphql.client import GraphQLClient
from my_app.core.logger import get_logger

log = get_logger(__name__)

# Global service instances
graphql_client: GraphQLClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    global graphql_client

    try:
        log_level_str = os.getenv("APP_LOG_LEVEL", "INFO").upper()
        log.info("=" * 60)
        log.info("My Project Name API Starting")
        log.info(f"Log Level: {log_level_str} ({logging.getLevelName(log.level)})")
        log.info("=" * 60)

        # Load configuration
        log.info("Loading configuration...")
        app_config = AppConfig()

        # Initialize GraphQL client
        log.info("Starting GraphQL client...")
        graphql_client = GraphQLClient(
            http_endpoint=app_config.http_endpoint,
            token_id=app_config.token_id,
            token_value=app_config.token_value,
        )
        await graphql_client.start()

        log.info("Application startup complete")

        yield

    finally:
        log.info("Shutting down services...")

        if graphql_client:
            await graphql_client.close()

        log.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="My Project Name API",
    description="My Project Name service",
    version="0.1.0",
    lifespan=lifespan,
    redirect_slashes=False,
)


@app.get("/", dependencies=[Depends(verify_bearer_token)])
async def root():
    """Root endpoint."""
    return {
        "message": "My Project Name API",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Global health check endpoint."""
    return {
        "status": "healthy",
        "graphql_client": graphql_client is not None,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    log.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn_config = UvicornConfig()

    uvicorn.run(
        "my_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=uvicorn_config.HOT_RELOAD,
        reload_excludes=[
            "logs/*",
            "debug_output/*",
            "*.log",
            ".idea/*",
            ".mypy_cache/*",
            ".pytest_cache/*",
            ".ruff_cache/*",
            ".venv/*",
            "__pycache__/*",
            "*.pyc",
            ".DS_Store",
            "*.md",
        ],
        log_level="info",
    )
