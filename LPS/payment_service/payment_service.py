#uvicorn payment_service:app --reload --port 8003
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Payment
from schemas import PaymentCreate, PaymentResponse
import random

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serviço de Pagamento")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/payments", response_model=PaymentResponse)
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # Simulação simples de sucesso/falha
    status = "pago" if random.random() > 0.1 else "falhou"

    db_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        method=payment.method,
        status=status
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment

@app.get("/payments/{order_id}", response_model=PaymentResponse)
def get_payment(order_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter_by(order_id=order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return payment
