from datetime import datetime
from unittest.mock import MagicMock
from pytest import fixture
from models.product import Product
from services.product_service import ProductService
from storages.product_storage import ProductStorage

@fixture   
def mock_cursor():
    return MagicMock()

@fixture
def mock_db(mock_cursor):
    mock_db = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_db

@fixture
def storage(mock_db):
    return ProductStorage(mock_db)

@fixture
def product(): 
    return Product(
        id = "01JFTE35ZRRZWCSKK6TBB1DZCT", 
        name = "cacau house",
        description = "bed for cats",
        price = 20.0,
        quantity = 100,
        active = True,
        created_at = datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at = None
    )
    
    
            