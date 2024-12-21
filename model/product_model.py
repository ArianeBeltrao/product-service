from typing import Optional
from datetime import datetime 
from pydantic import BaseModel, Field, model_validator

class Product(BaseModel):
        id: str
        name: str
        price: float = Field(gt=0, description="The price must be greater than zero")
        quantity: int
        active: bool = True
        description: str
        created_at: Optional[datetime] = None
        updated_at: Optional[datetime] = None
        @model_validator(mode='before')
        def set_created_at(cls, values):
            if values.get('created_at') is None:
                values['created_at'] = datetime.now()
            return values
              
        def __repr__(self):
            return f"Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity}, active={self.active}, description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"