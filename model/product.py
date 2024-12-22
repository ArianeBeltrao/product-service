from datetime import datetime 
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    description: str
    active: bool = True
    created_at: datetime = None
    updated_at: datetime = None