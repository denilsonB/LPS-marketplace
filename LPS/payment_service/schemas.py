from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str

class PaymentResponse(PaymentCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
