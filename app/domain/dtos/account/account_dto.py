from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class AccountCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class AccountDTO(AccountCreateDTO):
    id: UUID
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}