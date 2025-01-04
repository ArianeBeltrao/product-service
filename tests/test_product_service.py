from psycopg2 import DatabaseError
import pytest
from services.product_service import ProductService
from unittest.mock import MagicMock

mock_storage = MagicMock()
service = ProductService(mock_storage)

def test_get_all_products(product):
    mock_storage.get_all_products.return_value = [product]
    
    result = service.get_all_products()
    assert result == [product]
    mock_storage.get_all_products.assert_called_once()

def test_get_product_by_id(product) -> None:
    mock_storage.get_product_by_id.return_value = product
    
    result = service.get_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == product
    
def test_create_product(product):
    mock_storage.create_product.return_value = product
    
    result = service.create_product(product)
    assert result == product
    
def test_update_product(product):
    mock_storage.update_product.return_value = product
    
    result = service.update_product(product)
    assert result.updated_at != None
    
def test_delete_product():
    mock_storage.delete_product_by_id.return_value = None
    result = service.delete_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == None
    
def test_get_all_products_value_error():
    mock_storage.get_all_products.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        service.get_all_products()
    
def test_get_product_by_id_value_error() -> None:
    mock_storage.get_product_by_id.side_effect = ValueError()
    
    with pytest.raises(ValueError): #assert se a exception valueerror for jogada
        service.get_product_by_id('01JFTE35')
        
def test_create_product_value_error(product):
    mock_storage.create_product.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        service.create_product(product)
        
def test_update_product_value_error(product):
    mock_storage.update_product.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        service.update_product(product)
        
def test_delete_product_by_id_value_error():
    mock_storage.delete_product_by_id.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        service.delete_product_by_id('01JFTE35')
    