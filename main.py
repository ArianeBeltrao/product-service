from fastapi import FastAPI
from model.product import Product
import logging
from service.product_service import ProductService

logger = logging.getLogger(__name__)

app = FastAPI()

service = ProductService()

@app.get("/products/{id}")
async def get_product(id: str):
    logger.info(f"Started GetProduct with id={id}")
    product = service.get_product_by_id(id)
    logger.info(f"GetProduct request finished with response={product.model_dump()}")
    return product

@app.post("/products")
async def create_product(product: Product):
    logger.info(f"Started CreateProduct with body={product.model_dump()}")
    product_created = service.create_product(product)

    logger.info(f"CreateProduct request finished with response={product.model_dump()}")
    return product_created

