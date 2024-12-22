import logging
from model.product import Product
from .db_conn import db_connection

class ProductStorage: 
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection
    
    def save_product(self, product: Product) -> Product:
        self.logger.info("Inserting product in DB")
        try:
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
        except Exception as ex: 
            self.logger.error(f"Failed to insert product in DB. Error: {ex}")
            raise ex
        finally: 
            cursor.close()

        return product