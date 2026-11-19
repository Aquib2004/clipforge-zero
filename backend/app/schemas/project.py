"""Project request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    source_title: str | None = None
    source_creator: str | None = None
    source_url: str | None = None
    language: str = Field(default="en", min_length=2, max_length=10)
    output_location: str | None = None

    @field_validator("source_url")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        if v is None:
            return v
        from app.core.security import is_safe_url

        if not is_safe_url(v):
            raise ValueError("URL must use http or https scheme with a real host")
        return v


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    source_title: str | None = None
    source_creator: str | None = None
    source_url: str | None = None
    language: str | None = Field(None, min_length=2, max_length=10)
    status: str | None = None
    output_location: str | None = None


class ProjectRead(BaseModel):
    id: str
    name: str
    source_title: str | None
    source_creator: str | None
    source_url: str | None
    language: str
    status: str
    output_location: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectList(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
