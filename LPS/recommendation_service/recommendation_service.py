#uvicorn recommendation_service:app --reload --port 8005
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from collections import Counter

from database import SessionLocal, engine
from models import Base, PurchaseHistory
from schemas import PurchaseCreate, PurchaseResponse, RecommendationResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serviço de Recomendação de Produtos")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/purchases", response_model=PurchaseResponse)
def registrar_compra(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    compra = PurchaseHistory(
        customer_id=purchase.customer_id,
        product_id=purchase.product_id
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return compra

@app.get("/recommendations/{customer_id}", response_model=RecommendationResponse)
def recomendar_produtos(customer_id: int, db: Session = Depends(get_db)):
    # Histórico do cliente
    historico = db.query(PurchaseHistory).filter_by(customer_id=customer_id).all()
    if not historico:
        raise HTTPException(status_code=404, detail="Sem histórico de compras para este cliente")

    # Produtos que o cliente já comprou
    produtos_comprados: Set[int] = {p.product_id for p in historico}

    # Pega os produtos mais comprados por todos os usuários
    todos = db.query(PurchaseHistory).all()
    contagem = Counter([p.product_id for p in todos])

    # Remove os produtos que o usuário já comprou
    produtos_mais_comprados = [
        produto for produto, _ in contagem.most_common()
        if produto not in produtos_comprados
    ]

    # Retorna os top 5 produtos ainda não comprados
    produtos_recomendados = produtos_mais_comprados[:5]

    return RecommendationResponse(recommended_products=produtos_recomendados)