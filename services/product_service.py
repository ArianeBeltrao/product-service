import asyncio
import logging
import os
from datetime import datetime
from typing import List

import httpx
from dotenv import load_dotenv
from requests import RequestException

from models.product import Product, ProductAndCustomer
from storages.product_storage import ProductStorage


class ProductService:
    def __init__(self, storage: ProductStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        load_dotenv()

    async def get_all_products_and_customers(self) -> ProductAndCustomer:
        try:
            self.logger.info("Getting all products and customers...")

            all_products = self.storage.get_all_products()

            api_url = (
                f"{os.getenv("CUSTOMER_BASE_URL")}{os.getenv("CUSTOMER_GET_ALL_PATH")}"
            )

            self.logger.info("Calling customer service to get all customers")

            async with httpx.AsyncClient() as client:
                response = await client.get(api_url)
                all_customers = response.json()
                self.logger.debug(f"Customer data: {all_customers}")

                return ProductAndCustomer(
                    products=await all_products, customers=all_customers
                )

            batch = asyncio.gather(all_products, all_customers)

        except RequestException as e:
            self.logger.error(f"Failed to get customers: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to get products and customers: {e}")
            raise

    def get_all_products(self) -> List[Product]:
        self.logger.info("Getting all products...")
        return self.storage.get_all_products()

    def get_product_by_id(self, id: str) -> Product:
        self.logger.info("Getting product by id...")
        return self.storage.get_product_by_id(id)

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
