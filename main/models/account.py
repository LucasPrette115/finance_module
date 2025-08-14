
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.db.session import Base, SessionLocal

class Account(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
def get_all_accounts():
    session = SessionLocal()
    try:
        return session.query(Account).all()          
    finally:
        session.close()
        
        
def get_account_by_filter(filter_expr):
    
    session = SessionLocal()
    try:
        return session.query(Account).filter(filter_expr)
    finally:
        session.close()