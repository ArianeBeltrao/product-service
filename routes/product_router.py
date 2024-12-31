from fastapi import APIRouter, Depends, Request
from models.product import Product
import logging
from typing import Annotated, List
from services.product_service import ProductService

router = APIRouter()

logger = logging.getLogger(__name__)

def get_product_service(request: Request):
    return request.state.product_service

ServiceDep = Annotated[ProductService, Depends(get_product_service)]

@router.get("/products", response_model = List[Product])
def get_all_products(service: ServiceDep):
    logger.info(f"Started GetAllProducts")
    products_list: List[Product] = service.get_all_products()
    
    logger.info(f"GetAllProducts request finished with response={products_list}")
    return products_list

@router.get("/products/{id}", response_model=Product)
def get_product(id: str, service: ServiceDep):
    logger.info(f"Started GetProduct with id={id}")
    product = service.get_product_by_id(id)
    
    logger.info(f"GetProduct request finished with response={product.model_dump()}")
    return product

@router.post("/products", response_model=Product)
def create_product(product: Product, service: ServiceDep):
    logger.info(f"Started CreateProduct with body={product.model_dump()}")
    product_created = service.create_product(product)

    logger.info(f"CreateProduct request finished with response={product.model_dump()}")
    return product_created

@router.put("/products", response_model=Product)
def update_product(product: Product, service: ServiceDep):
    logger.info(f"Started UpdateProduct with body={product.model_dump()}")
    product_updated = service.update_product(product)
    
    logger.info(f"UpdateProduct request finished with response={product.model_dump()}")
    return product_updated
@router.delete("/products/{id}")
def delete_product(id: str, service: ServiceDep):
    logger.info(f"Started DeleteProduct with id={id}")
    service.delete_product_by_id(id)
    
    logger.info(f"DeleteProduct request finished for id={id}")
    return {"message": "Product deleted successfully"}
