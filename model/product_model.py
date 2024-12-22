from datetime import datetime 
from pydantic import BaseModel, Field
import ulid

class Product(BaseModel):
        id: str = Field(default_factory=lambda: str(ulid.new()))
        name: str
        price: float = Field(gt=0, description="The price must be greater than zero")
        quantity: int
        active: bool = True
        description: str
        created_at: datetime = Field(default_factory=datetime.now)
        updated_at: datetime = Field(default=None)