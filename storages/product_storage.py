import logging
from typing import List

from psycopg2 import DatabaseError
from psycopg2._psycopg import connection

from models.product import Product


class ProductStorage:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_all_products(self) -> List[Product]:
        self.logger.info("Getting all products in DB")
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT id, name, description, price, quantity, active, created_at, updated_at
                    FROM products
                    WHERE active = True
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                product_list = []

                for row in rows:
                    product = self.map_product_row_to_model(row)
                    product_list.append(product)

                return product_list
        except DatabaseError as ex:
            self.logger.error(f"Failed to get all products in DB. DatabaseError: {ex}")
            raise

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

                if result is None:
                    raise ValueError(f"Product not found with id {id}")

                return self.map_product_row_to_model(result)
        except DatabaseError as ex:
            self.logger.error(
                f"Failed to get product by id={id} in DB. DatabaseError: {ex}"
            )
            raise

    def create_product(self, product: Product) -> Product:
        self.logger.info("Inserting product in DB")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products 
                    (id, name, description, price, quantity, active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        product.id,
                        product.name,
                        product.description,
                        product.price,
                        product.quantity,
                        product.active,
                        product.created_at,
                    ),
                )
                self.db.commit()
                return product
        except DatabaseError as ex:
            self.logger.error(f"Failed to insert product in DB. DatabaseError: {ex}")
            self.db.rollback()
            raise

    def update_product(self, product: Product) -> Product:
        self.logger.info(f"Updating product in DB with ID {product.id}")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET 
                        name = %s,
                        description = %s,
                        price = %s,
                        quantity = %s,
                        active = %s,
                        updated_at = %s
                    WHERE id = %s
                    RETURNING id, name, description, price, quantity, active, created_at, updated_at
                    """,
                    (
                        product.name,
                        product.description,
                        product.price,
                        product.quantity,
                        product.active,
                        product.updated_at,
                        product.id,
                    ),
                )
                result = cursor.fetchone()

                if result is None:
                    raise ValueError(f"Product with ID {product.id} not found.")

            self.db.commit()
            return self.map_product_row_to_model(result)
        except DatabaseError as ex:
            self.logger.error(f"Failed on update operation. Error: {ex}")
            self.db.rollback()
            raise

    def delete_product_by_id(self, id: str) -> None:
        self.logger.info("Deleting product in DB")
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    DELETE FROM products
                    WHERE id = %s;
                """
                cursor.execute(sql_query, (id,))

                if cursor.rowcount == 0:
                    raise ValueError(f"Product not found with id {id}")

                self.db.commit()
        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(
                f"Failed to delete product by id={id} in DB. DatabaseError: {ex}"
            )
            raise

    def map_product_row_to_model(self, row: List) -> Product:
        return Product(
            id=row[0],
            name=row[1],
            description=row[2],
            price=row[3],
            quantity=row[4],
            active=row[5],
            created_at=row[6],
            updated_at=row[7],
        )
