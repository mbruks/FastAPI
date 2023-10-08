from fastapi import FastAPI
from pydantic import BaseModel, Field

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float