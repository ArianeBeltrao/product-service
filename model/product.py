from datetime import datetime 
import ulid
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int = Field(description="Product quantity")
    active: bool = Field(default=True, description="Product active status")
    created_at: datetime = Field(default_factory= datetime.now, description="Create product timestamp")
    updated_at: datetime | None = Field(default=None, description="Update product timestamp")