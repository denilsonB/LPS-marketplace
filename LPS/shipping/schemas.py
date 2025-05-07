from pydantic import BaseModel
from datetime import datetime

class ShippingCreate(BaseModel):
    order_id: int
    cep_destino: str

class ShippingResponse(ShippingCreate):
    id: int
    valor_frete: float
    status: str
    criado_em: datetime

    class Config:
        orm_mode = True
