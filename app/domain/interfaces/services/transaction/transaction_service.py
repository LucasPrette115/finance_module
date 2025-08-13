from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.dtos.transaction.transaction_dto import TransactionCreateDTO
from app.models.transaction import Transaction


class TransactionServiceInterface(ABC):
    @abstractmethod
    def create_transaction(self, tx: TransactionCreateDTO) -> Transaction: ...
    
    @abstractmethod
    def get_transaction_by_id(self, id: UUID) -> Optional[Transaction]: ...
    
    @abstractmethod
    def list_transactions_by_account(self, account_id: UUID) -> List[Transaction]: ...