# app/domain/interfaces/repositories/base_repository.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID
from typing import TYPE_CHECKING

T = TypeVar("T")

if TYPE_CHECKING:    
    from typing import Any

class BaseRepository(ABC, Generic[T]): 

    @abstractmethod
    def add(self, entity: "Any") -> T:
        """Adiciona uma entidade (p.ex. a partir de um DTO) e retorna a entidade persistida."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        """Retorna entidade por id ou None."""
        raise NotImplementedError

    @abstractmethod
    def list(self, offset: int = 0, limit: int = 100) -> List[T]:
        """Lista entidades com paginação simples."""
        raise NotImplementedError

    @abstractmethod
    def update(self, id: UUID, payload: "Any") -> T:
        """Atualiza a entidade com dados do payload e retorna a versão atualizada."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Remove a entidade (ou marca como excluída dependendo da política)."""
        raise NotImplementedError
