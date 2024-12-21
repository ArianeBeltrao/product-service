from model import Product
from storage.product_storage import ProductStorage

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()

    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.storage.save_product(product)
        return product
