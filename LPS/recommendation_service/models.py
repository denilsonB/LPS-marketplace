from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    product_id = Column(Integer)
    purchased_at = Column(DateTime, default=datetime.utcnow)
