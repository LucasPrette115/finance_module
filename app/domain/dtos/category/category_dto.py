from typing import Literal
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import  datetime

CategoryType = Literal["income", "expense", "transfer"]


class CategoryCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    type: CategoryType
    parent_id: Optional[UUID] = None

    model_config = {"from_attributes": True}


class CategoryDTO(CategoryCreateDTO):
    id: UUID
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}