#uvicorn order_service:app --reload --port 8002
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Order, OrderItem
from schemas import OrderCreate, OrderResponse
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serviço de Pedidos")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Pedido não pode estar vazio")

    total_price = sum(item.unit_price * item.quantity for item in order.items)
    db_order = Order(user_id=order.user_id, total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(order_item)

    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{user_id}", response_model=List[OrderResponse])
def list_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter_by(user_id=user_id).all()
