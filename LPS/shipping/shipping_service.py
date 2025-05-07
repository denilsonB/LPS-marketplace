#uvicorn shipping_service:app --reload --port 8004
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Shipping
from schemas import ShippingCreate, ShippingResponse
import random

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serviço de Frete")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_frete(cep: str) -> float:
    # Simulação simples: frete varia entre R$10 e R$30
    return round(random.uniform(10.0, 30.0), 2)

@app.post("/shippings", response_model=ShippingResponse)
def criar_envio(shipping: ShippingCreate, db: Session = Depends(get_db)):
    valor_frete = calcular_frete(shipping.cep_destino)

    db_shipping = Shipping(
        order_id=shipping.order_id,
        cep_destino=shipping.cep_destino,
        valor_frete=valor_frete,
        status="pendente"
    )

    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)

    return db_shipping

@app.get("/shippings/{order_id}", response_model=ShippingResponse)
def obter_envio(order_id: int, db: Session = Depends(get_db)):
    envio = db.query(Shipping).filter_by(order_id=order_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail="Envio não encontrado")
    return envio
