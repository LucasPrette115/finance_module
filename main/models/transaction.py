
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.session import Base, SessionLocal

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    date = Column(Date, nullable=False)
    description = Column(Text)
    document = Column(String(100))
    status = Column(String(50))
    credit = Column(Numeric(14,2), default=0)
    debit = Column(Numeric(14,2), default=0)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    

def map_financial_data_to_db(df, account_id):
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            transaction = Transaction(
                date=row['Data'],
                description=row['Descrição'],
                document=row['Docto'],
                status=row['Situação'],
                credit=row['Crédito (R$)'],
                debit=row['Débito (R$)'],
                account_id=account_id                     
            )
            session.add(transaction)
        session.commit() 
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        return False
    finally:
        session.close()

def get_all_transactions():
    session = SessionLocal()
    try:
        return session.query(Transaction).all()          
    finally:
        session.close()  