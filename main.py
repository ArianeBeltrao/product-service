from fastapi import FastAPI
from model.product import Product
import logging
from service.product_service import ProductService

logger = logging.getLogger(__name__)
# logger.basicConfig(level=logging.INFO)

app = FastAPI()

service = ProductService()

@app.post("/products")
async def create_product(product: Product):
    logger.info(f"Started CreateProduct with body={product.model_dump()}")
    product_created = service.create_product(product)
    logger.info(f"CreateProduct request finished with response={product.model_dump()}")
    return product_created

