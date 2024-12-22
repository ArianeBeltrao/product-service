import logging
from model.product import Product
from .db_conn import db_connection

class ProductStorage: 
    logger = logging.getLogger(__name__)
    db = db_connection
    
    def save_product(self, product: Product) -> Product:
        self.logger.info(f"Inserting product in DB")
        cursor = self.db.cursor()
        
        cursor.execute(f"""
            INSERT INTO products (id, name, description, price, quantity, active, created_at) 
            VALUES (
                '{product.id}', 
                '{product.name}', 
                '{product.description}', 
                {product.price}, 
                {product.quantity}, 
                {product.active}, 
                '{product.created_at}'
            );
            """)
        self.db.commit()
        cursor.close()
        return product