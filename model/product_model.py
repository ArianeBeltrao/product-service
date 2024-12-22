from datetime import datetime 
from pydantic import BaseModel, Field, model_validator

class Product(BaseModel):
        id: str
        name: str
        price: float = Field(gt=0, description="The price must be greater than zero")
        quantity: int
        active: bool = True
        description: str
        created_at: datetime = Field(default=None)
        updated_at: datetime = Field(default=None)
        @model_validator(mode='before')
        def set_created_at(cls, values):
            if values.get('created_at') is None:
                values['created_at'] = datetime.now()
            return values