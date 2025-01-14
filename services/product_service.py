import logging
from datetime import datetime
from typing import List

from models.product import Product
from storages.product_storage import ProductStorage


class ProductService:
    def __init__(self, storage: ProductStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage

    def get_all_products(self) -> List[Product]:
        self.logger.info("Getting all products...")
        return self.storage.get_all_products()

    def get_product_by_id(self, id: str) -> Product:
        self.logger.info("Getting product by id...")
        return self.storage.get_product_by_id(id)

    def get_product_by_name(self, name: str) -> Product:
        self.logger.info("Getting product by name...")
        return self.storage.get_product_by_name(name)

    def create_product(self, product: Product) -> Product:
        self.logger.info("Creating product...")
        return self.storage.create_product(product)

    def update_product(self, product: Product) -> Product:
        self.logger.info(f"Updating product with ID {id}...")
        product.updated_at = datetime.now()
        return self.storage.update_product(product)

    def delete_product_by_id(self, id: str) -> None:
        self.logger.info("Deleting product by id...")
        self.storage.delete_product_by_id(id)
