from datetime import datetime 
import ulid
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str
    price: float
    quantity: int
    description: str
    active: bool = True
    created_at: datetime = Field(default_factory= datetime.now)
    updated_at: datetime | None = Field(default=None)