
from app.domain.interfaces.repositories.transaction.transaction_repository import TransactionRepository
from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.domain.dtos.transaction.transaction_dto import TransactionCreateDTO, TransactionDTO
from sqlalchemy.orm import Session

class SqlAlchemyTransactionRepo(TransactionRepository):
    def __init__(self, db: Session = None):
        self._db = db or SessionLocal()

    def add(self, tx: TransactionCreateDTO) -> Transaction:
        model = Transaction(
            date=tx.date,
            description=tx.description,
            credit=tx.credit,
            debit=tx.debit,
            account_id=tx.account_id,
            category_id=tx.category_id
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model

    def get_by_id(self, id):
        row = self._db.query(Transaction).get(id)
        return row

    def list_by_account(self, account_id):
        rows = self._db.query(Transaction).filter_by(account_id=account_id).all()
        return rows
