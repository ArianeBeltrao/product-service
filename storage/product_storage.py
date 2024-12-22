import logging
from model.product import Product

class ProductStorage: 
    logger = logging.getLogger(__name__)
    
    def save_product(self, product: Product) -> Product:
        self.logger.info(f"Inserting product in DB")
        return product