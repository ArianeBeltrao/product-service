from fastapi import FastAPI
from model.product import Product
import logging

logger = logging.getLogger(__name__)
# logger.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/products")
async def create_product(product: Product):
    logger.info(f"started CreateProduct with body={product.model_dump()}")
    logger.info(f"CreateProduct request finished with response={product.model_dump()}")
    return product

