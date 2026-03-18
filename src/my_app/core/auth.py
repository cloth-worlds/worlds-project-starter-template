"""Authentication utilities for API endpoints."""

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from my_app.core.config import APIConfig

# Initialize security scheme
security = HTTPBearer()

# Load API config
api_config = APIConfig()


async def verify_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> None:
    """Verify the bearer token from the Authorization header."""
    token = credentials.credentials

    if not secrets.compare_digest(token, api_config.bearer_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
