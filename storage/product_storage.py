from model.product_model import Product

class ProductStorage:   
    def __init__(self):
        self.products = []

    def save_product(self, product: Product):
        self.products.append(product)
