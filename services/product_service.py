import logging
from models.product import Product
from typing import List
from storages.product_storage import ProductStorage
from datetime import datetime

class ProductService:
    
    def __init__(self, storage: ProductStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        
    def get_all_products(self) -> List[Product]:
        self.logger.info(f"Getting all products...") 
        return self.storage.get_all_products()
        
    def get_product_by_id(self, id: str) -> Product:
        self.logger.info(f"Getting product by id...") 
        return self.storage.get_product_by_id(id)
    
    def create_product(self, product: Product) -> Product:
        self.logger.info(f"Creating product...")
        return self.storage.save_product(product)
    
    def update_product(self, product: Product) -> Product:
        self.logger.info(f"Updating product with ID {id}...")
        product.updated_at = datetime.now()
        return self.storage.update_product(product)

    def update_product(self, product: Product) -> Product:
        self.logger.info(f"Updating product with ID {id}...")
        product.updated_at = datetime.now()
        return self.storage.update_product(product)

    def delete_product_by_id(self, id: str) -> None:
        self.logger.info(f"Deleting product by id...")
        self.storage.delete_product_by_id(id)
