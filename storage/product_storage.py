from psycopg2 import DatabaseError
import logging
from model.product import Product
from config.db_conn import db_connection

class ProductStorage: 
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection
    
    def get_product_by_id(self, id: str) -> Product:
        self.logger.info("Getting product in DB")
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT id, name, description, price, quantity, active, created_at, updated_at
                    FROM products
                    WHERE id = %s;
                """
            
                cursor.execute(sql_query, (id,))
                result = cursor.fetchone()
                
                if result == None:
                    # TODO add specific exception on next task 
                    raise Exception(f"Product not found with id {id}")
                
                return Product(
                    id = result[0],
                    name = result[1],
                    description = result[2],
                    price = result[3],
                    quantity = result[4],
                    active = result[5],
                    created_at = result[6],
                    updated_at = result[7]
                )
        except Exception as ex: 
            self.logger.error(f"Failed to get product by id={id} in DB. Error: {ex}")
            raise
    
    def save_product(self, product: Product) -> Product:
        self.logger.info("Inserting product in DB")
        try:
            with self.db.cursor() as cursor:
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
                return product
        except Exception as ex: 
            self.logger.error(f"Failed to insert product in DB. Error: {ex}")
            raise ex
        finally:
            self.db.commit()
            
    def update_product(self, product: Product) -> Product:
        self.logger.info(f"Updating product in DB with ID {product.id}")
        try:
            with self.db.cursor() as cursor:
                cursor.execute("""
                    UPDATE products
                    SET 
                        name = %s,
                        description = %s,
                        price = %s,
                        quantity = %s,
                        active = %s,
                        updated_at = %s
                    WHERE id = %s;
                    """, (product.name, product.description, product.price, product.quantity, product.active, product.updated_at, product.id))
            self.db.commit()          
            return self.get_product_by_id(product.id)
        except DatabaseError as ex:
            self.logger.error(f"Failed on update operation. Error: {ex}")
            self.db.rollback()
            raise 
            
        
