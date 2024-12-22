import logging
from model.product import Product
from storage.product_storage import ProductStorage

class ProductService:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = ProductStorage()
        
    def get_product_by_id(self, id: str) -> Product:
        self.logger.info(f"Getting product...") 
        return self.storage.get_product_by_id(id)
    
    def create_product(self, product: Product) -> Product:
        self.logger.info(f"Creating product...")
        return self.storage.save_product(product)