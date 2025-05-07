from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]

class OrderItemResponse(OrderItemCreate):
    id: int
    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
