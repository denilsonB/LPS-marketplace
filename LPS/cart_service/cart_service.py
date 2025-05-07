#uvicorn cart_service:app --reload --port 8001
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, CartItem
from schemas import CartItemCreate, CartItemResponse
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serviço de Carrinho")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cart/{user_id}/items", response_model=CartItemResponse)
def add_to_cart(user_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    existing = db.query(CartItem).filter_by(user_id=user_id, product_id=item.product_id).first()
    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing
    cart_item = CartItem(user_id=user_id, **item.dict())
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@app.get("/cart/{user_id}/items", response_model=List[CartItemResponse])
def list_cart_items(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter_by(user_id=user_id).all()

@app.delete("/cart/{user_id}/items/{product_id}")
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não está no carrinho")
    db.delete(item)
    db.commit()
    return {"detail": "Produto removido do carrinho"}

@app.delete("/cart/{user_id}/clear")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    db.query(CartItem).filter_by(user_id=user_id).delete()
    db.commit()
    return {"detail": "Carrinho limpo com sucesso"}
