from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Shipping(Base):
    __tablename__ = "shippings"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    cep_destino = Column(String)
    valor_frete = Column(Float)
    status = Column(String, default="pendente")  # pendente, enviado, entregue
    criado_em = Column(DateTime, default=datetime.utcnow)
