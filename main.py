from fastapi import FastAPI
from route.product_router import router as product_router
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(product_router)