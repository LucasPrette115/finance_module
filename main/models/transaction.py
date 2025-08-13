import uuid
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())