"""Common schemas used across the API."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    code: str
    detail: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"
