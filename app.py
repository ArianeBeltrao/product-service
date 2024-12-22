from fastapi import FastAPI
from service.product_service import ProductService
from model.product_model import Product

app = FastAPI()
product_service = ProductService()

@app.post("/products/", response_model=Product)
def create_product(product_data: Product):
    product = product_service.create_product(product_data.dict())
    return product
