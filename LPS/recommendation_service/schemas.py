from pydantic import BaseModel
from datetime import datetime
from typing import List

class PurchaseCreate(BaseModel):
    customer_id: int
    product_id: int

class PurchaseResponse(PurchaseCreate):
    id: int
    purchased_at: datetime

    class Config:
        orm_mode = True

class RecommendationResponse(BaseModel):
    recommended_products: List[int]
