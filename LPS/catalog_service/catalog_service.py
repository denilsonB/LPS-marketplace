"""
para rodar a api usar:
pip install -r requirements.txt
uvicorn catalog_service:app --reload
uvicorn catalog_service:app --host 0.0.0.0 --port 8000 # formato passando a porta


URL's aceitas:
GET http://localhost:8000/products para listar todos os produtos
POST http://localhost:8000/products para criar um produto
GET http://localhost:8000/products/id para ver um produto especifico
PUT http://localhost:8000/products/id para atualizar um produto especifico
DELETE http://localhost:8000/products/id para deletar um produto especifico 
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
from models import Base, Product

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catálogo de Produtos")

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductResponse(ProductCreate):
    id: int
    class Config:
        orm_mode = True

# Dependência para injeção do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}
