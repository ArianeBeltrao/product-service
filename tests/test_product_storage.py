from datetime import datetime
from decimal import Decimal
from psycopg2 import DatabaseError
import pytest

def test_get_all_products(mock_cursor, storage, product):
    mock_cursor.fetchall.return_value = [
        (
            "01JFTE35ZRRZWCSKK6TBB1DZCT", 
            "cacau house",
            "bed for cats",
            Decimal('20.0'),
            100,
            True,
            datetime(2024, 12, 23, 15, 57, 25, 496623),
            None
        )
    ]
    
    result = storage.get_all_products()
    assert result == [product]
    
    mock_cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, quantity, active, created_at, updated_at
            FROM products
            WHERE active = True 
        """
    )

def test_get_product_by_id(mock_cursor, storage, product):
    mock_cursor.fetchone.return_value = (
        "01JFTE35ZRRZWCSKK6TBB1DZCT", 
        "cacau house",
        "bed for cats",
        Decimal('20.0'),
        100,
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        None
    )

    result = storage.get_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == product
    
    mock_cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, description, price, quantity, active, created_at, updated_at
        FROM products
        WHERE id = %s;
        """, ('01JFTE35ZRRZWCSKK6TBB1DZCT',)
    )
    
def test_create_product(mock_cursor, storage, product):
    result = storage.create_product(product)

    assert result == product
    
    mock_cursor.execute.assert_called_once_with
    (
    """
        INSERT INTO products (id, name, description, price, quantity, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (product.id, product.name, product.description, product.price, product.quantity, product.active, product.created_at)
    )

def test_update_product(mock_cursor, storage, product):
    product.updated_at = datetime(2025, 12, 23, 15, 57, 25, 496623)
    
    mock_cursor.fetchone.return_value = (
        "01JFTE35ZRRZWCSKK6TBB1DZCT", 
        "cacau house",
        "bed for cats",
        Decimal('20.0'),
        100,
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        datetime(2025, 12, 23, 15, 57, 25, 496623)
    )
    
    result = storage.update_product(product)
    assert result == product
    
    mock_cursor.execute.assert_called_once_with
    (
        """
            UPDATE products
            SET 
                name = %s,
                description = %s,
                price = %s,
                quantity = %s,
                active = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id, name, description, price, quantity, active, created_at, updated_at
        """, (product.name, product.description, product.price, product.quantity, product.active, product.updated_at, product.id)
    )
    
def test_delete_product_by_id(mock_cursor, storage):
    mock_cursor.rowcount = 1
    
    result = storage.delete_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    assert result == None
    
    mock_cursor.execute.assert_called_once_with
    (
        """
            DELETE FROM products
            WHERE id = %s;
        """, ('01JFTE35ZRRZWCSKK6TBB1DZCT',)   
    )
    
def test_get_all_products_database_error(mock_cursor, storage):
    mock_cursor.execute.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        storage.get_all_products()
        
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_not_called()

def test_get_product_by_id_value_error(mock_cursor, storage):
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(ValueError):
        storage.get_product_by_id('01JFTE35ZRRZWCSKK6TBB1DZCT')
    
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
        
def test_create_product_database_error(mock_cursor, storage, product):
    mock_cursor.execute.side_effect = DatabaseError()
    
    with pytest.raises(DatabaseError):
        storage.create_product(product)

    mock_cursor.execute.assert_called_once()
        
def test_update_product_value_error(mock_cursor, storage, product):
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(ValueError):
        storage.update_product(product)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()
        
def test_delete_product_by_id(mock_cursor, storage):
    mock_cursor.rowcount = 0
    
    with pytest.raises(ValueError):
        storage.delete_product_by_id('01JFTE35')

    mock_cursor.execute.assert_called_once()
        
