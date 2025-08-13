from __future__ import annotations
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from app.domain.dtos.transaction.transaction_dto import TransactionCreateDTO
from app.domain.interfaces.repositories.transaction.transaction_repository import TransactionRepositoryInterface
from app.domain.interfaces.services.transaction.transaction_service import TransactionServiceInterface
from app.models.transaction import Transaction


class TransactionService(TransactionServiceInterface):
    def __init__(self, transaction_repository: TransactionRepositoryInterface):
        self._transaction_repository = transaction_repository

    def create_transaction(self, dto: TransactionCreateDTO) -> Transaction:
        """
        Cria uma transação após validar regras de negócio mínimas:
          - deve ser crédito OR débito (XOR)
          - (ponto de extensão) validar existência de account_id/category_id, saldo, etc.
        Retorna a instância Transaction criada pelo repositório.
        """
        # Use Decimal para comparações seguras com valores monetários
        zero = Decimal("0")
        credit = dto.credit if isinstance(dto.credit, Decimal) else Decimal(str(dto.credit))
        debit = dto.debit if isinstance(dto.debit, Decimal) else Decimal(str(dto.debit))

        if (credit > zero and debit > zero) or (credit == zero and debit == zero):
            raise ValueError("Transação deve ser crédito ou débito, não ambos/neutro")

        # >>> Aqui você pode adicionar outras validações:
        # - verificar se account existe (via outro repo ou método do transaction_repository)
        # - verificar se category existe (se category_id fornecido)
        # - checar saldo disponível (se aplicável)
        # - normalizar campos (trim em descrição, etc.)

        # Delega ao repositório para persistência (assume-se que repo.add retorna Transaction)
        created = self._transaction_repository.add(dto)
        return created

    def get_transaction_by_id(self, id: UUID) -> Optional[Transaction]:
        """
        Busca transação por id. Retorna None se não existir (interface permitia Optional).
        Caso prefira lançar exceção, faça a checagem aqui e levante NotFoundError.
        """
        return self._transaction_repository.get_by_id(id)

    def list_transactions_by_account(self, account_id: UUID) -> List[Transaction]:
        """
        Lista todas as transações associadas a uma conta.
        (Se quiser paginação/filtros, adicione parâmetros offset/limit/start_date/end_date etc.)
        """
        return self._transaction_repository.list_by_account(account_id)
