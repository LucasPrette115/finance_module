from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.dtos.category.category_dto import CategoryCreateDTO, CategoryDTO

class CategoryServiceInterface(ABC):   

    @abstractmethod
    def create(self, payload: CategoryCreateDTO) -> CategoryDTO: ...     

    @abstractmethod
    def get(self, category_id: UUID) -> CategoryDTO: ...

    @abstractmethod
    def list(self, type_filter: Optional[str] = None, offset: int = 0, limit: int = 100) -> List[CategoryDTO]: ...

    @abstractmethod
    def update(self, category_id: UUID, payload: CategoryCreateDTO) -> CategoryDTO: ...

    @abstractmethod
    def delete(self, category_id: UUID) -> None: ...