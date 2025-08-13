from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID
import pandas as pd

class TransactionCreateDTO(BaseModel):
    date: date
    description: Optional[str]
    credit: float = 0.0
    debit: float = 0.0
    account_id: UUID
    category_id: Optional[UUID]
    
class TransactionDTO(TransactionCreateDTO):
    id: UUID
    created_at: Optional[str]

    model_config = {
        "from_attributes": True
    }
    
    def map(df):
        transactions = [
            TransactionCreateDTO(
                date=row['Data'],
                description=row['Descrição'],
                credit=row['Crédito (R$)'] if not pd.isna(row['Crédito (R$)']) else 0.0,
                debit=row['Débito (R$)'] if not pd.isna(row['Débito (R$)']) else 0.0,
                account_id=row.get('account_id'),
                category_id=row.get('category_id')
            )
            for _, row in df.iterrows()
        ]
        return transactions