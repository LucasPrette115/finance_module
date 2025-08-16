
import pandas as pd
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.session import Base, SessionLocal
from models.account import Account

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    date = Column(Date, nullable=False)
    description = Column(Text)
    document = Column(String(100))
    status = Column(String(50))
    credit = Column(Numeric(14,2), default=0)
    debit = Column(Numeric(14,2), default=0)
    balance = Column(Numeric(14,2), default=0)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    

def map_financial_data_to_db(df, account_id):
    session = SessionLocal()
    try:
        transactions = []       

        for _, row in df.iterrows():
            transaction = Transaction(
                date=row['Data'],
                description=row['Descrição'],
                document=row['Docto'],
                status=row['Situação'],
                credit=row['Crédito (R$)'],
                debit=row['Débito (R$)'],
                balance=row['Saldo (R$)'],
                account_id=account_id
            )
            transactions.append(transaction)

        session.add_all(transactions)
        session.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        return False
    finally:
        session.close()

def get_all_transactions(selected_accounts):
    session = SessionLocal()
    try:
        transactions = session.query(Transaction).all()  
        accounts = {
            acc.id: acc.name
            for acc in session.query(Account)
            .filter(Account.id.in_(selected_accounts))
        } 
        data = [
            {                
                "Data": t.date,
                "Descrição": t.description,
                "Docto": t.document,
                "Situação": t.status,
                "Crédito (R$)": t.credit,
                "Débito (R$)": -t.debit,
                "Saldo (R$)": t.balance,
                "Conta": accounts[t.account_id]
            }
            for t in transactions
        ]
        return pd.DataFrame(data)
    finally:
        session.close() 