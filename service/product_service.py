import logging
from model.product import Product
from storage.product_storage import ProductStorage

class ProductService:
    logger = logging.getLogger(__name__)
    
    storage = ProductStorage()
    
    def create_product(self, product: Product) -> Product:
        self.logger.info(f"Creating product...")
        product_created = self.storage.save_product(product)
        return product_created