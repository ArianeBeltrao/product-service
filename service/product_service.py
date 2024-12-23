import logging
from model.product import Product
from storage.product_storage import ProductStorage
from typing import List

class ProductService:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = ProductStorage()
        
    def get_all_products(self) -> List[Product]:
        self.logger.info(f"Getting all products...") 
        return self.storage.get_all_products()
        
    def get_product_by_id(self, id: str) -> Product:
        self.logger.info(f"Getting product by id...") 
        return self.storage.get_product_by_id(id)
    
    def create_product(self, product: Product) -> Product:
        self.logger.info(f"Creating product...")
        return self.storage.save_product(product)