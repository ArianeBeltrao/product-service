from fastapi import APIRouter
from model.product import Product
import logging
from service.product_service import ProductService
from typing import List

router = APIRouter()

logger = logging.getLogger(__name__)
service = ProductService()

@router.get("/products", response_model=List[Product])
def get_all_products():
    logger.info(f"Started GetAllProducts")
    products_list: List[Product] = service.get_all_products()
    
    logger.info(f"GetAllProducts request finished with response={products_list}")
    return products_list


@router.get("/products/{id}", response_model=Product)
def get_product(id: str):
    logger.info(f"Started GetProduct with id={id}")
    product = service.get_product_by_id(id)
    
    logger.info(f"GetProduct request finished with response={product.model_dump()}")
    return product

@router.post("/products", response_model=Product)
def create_product(product: Product):
    logger.info(f"Started CreateProduct with body={product.model_dump()}")
    product_created = service.create_product(product)

    logger.info(f"CreateProduct request finished with response={product.model_dump()}")
    return product_created

@router.put("/products", response_model=Product)
async def update_product(product: Product):
    logger.info(f"Started UpdateProduct with body={product.model_dump()}")
    product_updated = service.update_product(product)
    
    logger.info(f"UpdateProduct request finished with response={product.model_dump()}")
    return product_updated