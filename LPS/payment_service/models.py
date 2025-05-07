from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    amount = Column(Float)
    status = Column(String, default="pendente")  # pendente, pago, falhou
    method = Column(String)  # ex: "cartão", "boleto", etc.
    created_at = Column(DateTime, default=datetime.utcnow)
