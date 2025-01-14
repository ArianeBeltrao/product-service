from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from psycopg2 import DatabaseError
from pytest import fixture

from storages.product_storage import ProductStorage


@fixture(name="cursor")
def fixture_cursor():
    """
    Creates a mock cursor object to simulate database interactions.

    Returns:
        MagicMock: A mock cursor object.
    """
    return MagicMock()


@fixture(name="db_conn")
def fixture_db_conn(cursor):
    """
    Creates a mock database connection object with a mock cursor.

    Args:
        cursor (MagicMock): A mock cursor object.

    Returns:
        MagicMock: A mock database connection object.
    """
    db_conn = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor
    return db_conn


@fixture(name="storage")
def fixture_storage(db_conn):
    """
    Creates an instance of ProductStorage with a mock database connection.

    Args:
        db_conn (MagicMock): A mock database connection object.

    Returns:
        ProductStorage: A storage instance using the mock database connection.
    """
    return ProductStorage(db_conn)


@fixture(name="product_row")
def fixture_product_row():
    """
    Provides a sample product row for testing database operations.

    Returns:
        tuple: A tuple representing a product row.
    """
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


@fixture(name="updated_product_row")
def fixture_updated_product_row():
    """
    Provides a sample updated product row for testing.

    Returns:
        tuple: A tuple representing a product with updated fields.
    """
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


def test_get_all_products(cursor, storage, product, product_row):
    """
    Test that `get_all_products` retrieves all active products from the database
    and maps the results to the expected product model.
    """
    cursor.fetchall.return_value = [product_row]

    result = storage.get_all_products()
    assert result == [product]

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, quantity, active, created_at, updated_at
            FROM products
            WHERE active = True 
        """
    )


def test_get_product_by_id(cursor, storage, product, product_row):
    """
    Test that `get_product_by_id` retrieves a product by ID from the database
    and maps the result to the expected product model.
    """
    cursor.fetchone.return_value = product_row

    result = storage.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result == product

    cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, description, price, quantity, active, created_at, updated_at
        FROM products
        WHERE id = %s;
        """,
        ("01JFTE35ZRRZWCSKK6TBB1DZCT",),
    )


def test_create_product(cursor, db_conn, storage, product):
    """
    Test that `create_product` inserts a new product into the database
    and returns the created product object.
    """
    result = storage.create_product(product)

    assert result == product

    db_conn.commit.assert_called_once()

    cursor.execute.assert_called_once_with
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


def test_update_product(cursor, storage, product, updated_product_row, db_conn):
    """
    Test that `update_product` updates an existing product in the database
    and returns the updated product object.
    """
    product.updated_at = datetime(2025, 12, 23, 15, 57, 25, 496623)

    cursor.fetchone.return_value = updated_product_row

    result = storage.update_product(product)
    assert result == product

    db_conn.commit.assert_called_once()

    cursor.execute.assert_called_once_with
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


def test_delete_product_by_id(cursor, storage, db_conn):
    """
    Test that `delete_product_by_id` removes a product from the database
    by its ID when the ID exists.
    """
    cursor.rowcount = 1

    result = storage.delete_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result is None

    db_conn.commit.assert_called_once()

    cursor.execute.assert_called_once_with
    (
        """
            DELETE FROM products
            WHERE id = %s;
        """,
        ("01JFTE35ZRRZWCSKK6TBB1DZCT",),
    )


def test_get_all_products_database_error(cursor, storage):
    """
    Test that `get_all_products` raises a `DatabaseError`
    when an error occurs during query execution.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_all_products()

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_not_called()


def test_get_product_by_id_value_error(cursor, storage):
    """
    Test that `get_product_by_id` raises a `ValueError`
    when the product with the given ID does not exist in the database.
    """
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    cursor.execute.assert_called_once()
    cursor.fetchone.assert_called_once()


def test_get_product_by_id_database_error(cursor, storage):
    """
    Test that `get_product_by_id` raises a `DatabaseError`
    when a database error occurs during the query execution.

    Verifies that the cursor's `execute` method is called exactly once.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    cursor.execute.assert_called_once()


def test_create_product_database_error(cursor, storage, product, db_conn):
    """
    Test that `create_product` raises a `DatabaseError`
    when an error occurs during the insertion of a new product.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.create_product(product)

    cursor.execute.assert_called_once()

    db_conn.rollback.assert_called_once()


def test_update_product_value_error(cursor, storage, product, db_conn):
    """
    Test that `update_product` raises a `ValueError`
    when the product with the given ID does not exist in the database.
    """
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.update_product(product)

    cursor.execute.assert_called_once()
    cursor.fetchone.assert_called_once()

    db_conn.commit.assert_not_called()


def test_update_product_database_error(storage, cursor, product, db_conn):
    """
    Test that `update_product` raises a `DatabaseError`
    when a database error occurs during the update operation.

    Verifies that the cursor's `execute` method is called exactly once
    and that a rollback is performed on the database connection.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.update_product(product)

    cursor.execute.assert_called_once()

    db_conn.rollback.assert_called_once()


def test_delete_product_by_id_value_error(cursor, storage, db_conn):
    """
    Test that `delete_product_by_id` raises a `ValueError`
    when attempting to delete a product with a non-existing ID.
    """
    cursor.rowcount = 0

    with pytest.raises(ValueError):
        storage.delete_product_by_id("01JFTE35")

    cursor.execute.assert_called_once()

    db_conn.commit.assert_not_called()


def test_delete_product_by_id_database_error(cursor, storage, db_conn):
    """
    Test that `delete_product_by_id` raises a `DatabaseError`
    when a database error occurs during the deletion operation.

    Verifies that the cursor's `execute` method is called exactly once
    and that a rollback is performed on the database connection.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.delete_product_by_id("01JFTE35")

    cursor.execute.assert_called_once()

    db_conn.rollback.assert_called_once()
