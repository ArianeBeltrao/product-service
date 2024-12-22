from model.product_model import Product
from storage.product_storage import ProductStorage

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()

    def create_product(self, product: Product) -> Product:
        self.storage.save_product(product)
        return product
