from datetime import datetime 

class Product:
    def __init__(self, id: str, name: str, price: float, quantity: int, description: str, active: bool = True, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = active
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at
        

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity}, active={self.active}, description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"