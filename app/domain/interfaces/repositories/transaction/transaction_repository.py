from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.transaction import Transaction
from app.domain.dtos.transaction.transaction_dto import TransactionCreateDTO

class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def add(self, tx: TransactionCreateDTO) -> Transaction: ...
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Transaction]: ...
    @abstractmethod
    def list_by_account(self, account_id: UUID) -> List[Transaction]: ...