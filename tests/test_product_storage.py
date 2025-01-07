from datetime import datetime
from decimal import Decimal

import pytest
from psycopg2 import DatabaseError


@pytest.fixture
def product_row():
    return (
        "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "cacau house",
        "bed for cats",
        Decimal("20.0"),
        100,
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        None,
    )


@pytest.fixture
def updated_product_row():
    return (
        "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "cacau house",
        "bed for cats",
        Decimal("20.0"),
        100,
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        datetime(2025, 12, 23, 15, 57, 25, 496623),
    )


def test_get_all_products(mock_cursor, storage, product, product_row):
    """
    Test that `get_all_products` retrieves all active products from the database
    and maps the results to the expected product model.
    """
    mock_cursor.fetchall.return_value = [product_row]

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


def test_get_product_by_id(mock_cursor, storage, product, product_row):
    """
    Test that `get_product_by_id` retrieves a product by ID from the database
    and maps the result to the expected product model.
    """
    mock_cursor.fetchone.return_value = product_row

    result = storage.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result == product

    mock_cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, description, price, quantity, active, created_at, updated_at
        FROM products
        WHERE id = %s;
        """,
        ("01JFTE35ZRRZWCSKK6TBB1DZCT",),
    )


def test_create_product(mock_cursor, storage, product):
    """
    Test that `create_product` inserts a new product into the database
    and returns the created product object.
    """
    result = storage.create_product(product)

    assert result == product

    mock_cursor.execute.assert_called_once_with
    (
        """
        INSERT INTO products (id, name, description, price, quantity, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """,
        (
            product.id,
            product.name,
            product.description,
            product.price,
            product.quantity,
            product.active,
            product.created_at,
        ),
    )


def test_update_product(mock_cursor, storage, product, updated_product_row):
    """
    Test that `update_product` updates an existing product in the database
    and returns the updated product object.
    """
    product.updated_at = datetime(2025, 12, 23, 15, 57, 25, 496623)

    mock_cursor.fetchone.return_value = updated_product_row

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
        """,
        (
            product.name,
            product.description,
            product.price,
            product.quantity,
            product.active,
            product.updated_at,
            product.id,
        ),
    )


def test_delete_product_by_id(mock_cursor, storage):
    """
    Test that `delete_product_by_id` removes a product from the database
    by its ID when the ID exists.
    """
    mock_cursor.rowcount = 1

    result = storage.delete_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result is None

    mock_cursor.execute.assert_called_once_with
    (
        """
            DELETE FROM products
            WHERE id = %s;
        """,
        ("01JFTE35ZRRZWCSKK6TBB1DZCT",),
    )


def test_get_all_products_database_error(mock_cursor, storage):
    """
    Test that `get_all_products` raises a `DatabaseError`
    when an error occurs during query execution.
    """
    mock_cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_all_products()

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_not_called()


def test_get_product_by_id_value_error(mock_cursor, storage):
    """
    Test that `get_product_by_id` raises a `ValueError`
    when the product with the given ID does not exist in the database.
    """
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()


def test_create_product_database_error(mock_cursor, storage, product):
    """
    Test that `create_product` raises a `DatabaseError`
    when an error occurs during the insertion of a new product.
    """
    mock_cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.create_product(product)

    mock_cursor.execute.assert_called_once()


def test_update_product_value_error(mock_cursor, storage, product):
    """
    Test that `update_product` raises a `ValueError`
    when the product with the given ID does not exist in the database.
    """
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.update_product(product)

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()


def test_delete_product_by_id_value_error(mock_cursor, storage):
    """
    Test that `delete_product_by_id` raises a `ValueError`
    when attempting to delete a product with a non-existing ID.
    """
    mock_cursor.rowcount = 0

    with pytest.raises(ValueError):
        storage.delete_product_by_id("01JFTE35")

    mock_cursor.execute.assert_called_once()
