from psycopg2 import DatabaseError
import pytest
from pytest import fixture
from services.product_service import ProductService
from unittest.mock import MagicMock

@fixture
def mock_storage():
    return MagicMock()

@fixture
def service(mock_storage):
    return ProductService(mock_storage)


def test_get_all_products(product, mock_storage, service):
    mock_storage.get_all_products.return_value = [product]
    
    result = service.get_all_products()
    assert result == [product]
    mock_storage.get_all_products.assert_called_once()

def test_get_product_by_id(product, mock_storage, service) -> None:
    mock_storage.get_product_by_id.return_value = product
    
    result = service.get_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == product
    mock_storage.get_product_by_id.assert_called_once_with('01JFTE35ZRRZWCSKK6TBB1DZCT')
    
def test_create_product(product, mock_storage, service):
    mock_storage.create_product.return_value = product
    
    result = service.create_product(product)
    assert result == product
    mock_storage.create_product.assert_called_once_with(product)
    
def test_update_product(product, mock_storage, service):
    mock_storage.update_product.return_value = product
    
    result = service.update_product(product)
    assert result.updated_at != None
    mock_storage.update_product.assert_called_once_with(product)
    
def test_delete_product(mock_storage, service):
    mock_storage.delete_product_by_id.return_value = None
    result = service.delete_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == None
    mock_storage.delete_product_by_id.assert_called_once_with('01JFTE35ZRRZWCSKK6TBB1DZCT')
    
def test_get_all_products_database_error(mock_storage, service):
    mock_storage.get_all_products.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        service.get_all_products()
        
    mock_storage.get_all_products.assert_called_once()
    
def test_get_product_by_id_value_error(mock_storage, service) -> None:
    mock_storage.get_product_by_id.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        service.get_product_by_id('01JFTE35')
        
    mock_storage.get_product_by_id.assert_called_once_with('01JFTE35')
        
def test_create_product_value_error(product, mock_storage, service):
    mock_storage.create_product.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        service.create_product(product)
        
    mock_storage.create_product.assert_called_once_with(product)
        
def test_update_product_value_error(product, mock_storage, service):
    mock_storage.update_product.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        service.update_product(product)
        
    mock_storage.update_product.assert_called_once_with(product)
        
def test_delete_product_by_id_value_error(mock_storage, service):
    mock_storage.delete_product_by_id.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        service.delete_product_by_id('01JFTE35')
        
    mock_storage.delete_product_by_id.assert_called_once_with('01JFTE35')
    