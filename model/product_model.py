from datetime import datetime 
from pydantic import BaseModel, Field

class Product(BaseModel):
        id: str
        name: str
        price: float = Field(gt=0, description="The price must be greater than zero")
        quantity: int
        active: bool = True
        description: str
        created_at: datetime = Field(default_factory=datetime.now)
        updated_at: datetime = Field(default=None)
