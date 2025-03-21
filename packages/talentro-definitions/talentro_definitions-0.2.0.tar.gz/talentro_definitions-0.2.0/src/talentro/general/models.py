import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, default=datetime.now())
    updated_at: datetime = Field(nullable=True)


class ClintBaseModel(BaseModel):
    company_id: str = Field(index=True)
