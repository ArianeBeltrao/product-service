from datetime import datetime 
import ulid
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str
    description: str
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory= datetime.now)
    updated_at: datetime | None = Field(default=None)