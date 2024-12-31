from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db_conn import get_database_connection
from route.product_router import router
import logging
from service.product_service import ProductService
from storage.product_storage import ProductStorage

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    product_storage = ProductStorage(db_connection=db_connection)
    product_service = ProductService(product_storage)

    yield {"product_service": product_service}
    logger.info(f"Shutdown application")
    
app = FastAPI(lifespan=lifespan, title="Product Service",)
app.include_router(router)