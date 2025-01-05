from unittest.mock import MagicMock

import pytest
from psycopg2 import DatabaseError
from pytest import fixture

from services.product_service import ProductService


@fixture
def mock_storage():
    return MagicMock()


@fixture
def service(mock_storage):
    return ProductService(mock_storage)


def test_retrieve_all_products_successfully(product, mock_storage, service):
    """
    Tests that the `get_all_products` method correctly retrieves a list of products
    from the underlying storage service.
    """
    mock_storage.get_all_products.return_value = [product]

    result = service.get_all_products()
    assert result == [product]
    mock_storage.get_all_products.assert_called_once()


def test_retrieve_product_by_id_successfully(product, mock_storage, service):
    """
    Tests that the `get_product_by_id` method retrieves the correct product
    when a valid product ID is provided.
    """
    mock_storage.get_product_by_id.return_value = product

    result = service.get_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result == product
    mock_storage.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_create_product_successfully(product, mock_storage, service):
    """
    Tests that the `create_product` method successfully creates a product
    and returns the created product.
    """
    mock_storage.create_product.return_value = product

    result = service.create_product(product)
    assert result == product
    mock_storage.create_product.assert_called_once_with(product)


def test_update_product_successfully(product, mock_storage, service):
    """
    Tests that the `update_product` method successfully updates a product
    and verifies that the `updated_at` field is modified.
    """
    mock_storage.update_product.return_value = product

    result = service.update_product(product)
    assert result.updated_at is not None
    mock_storage.update_product.assert_called_once_with(product)


def test_delete_product_by_id_successfully(mock_storage, service):
    """
    Tests that the `delete_product_by_id` method successfully deletes a product
    when a valid product ID is provided.
    """
    mock_storage.delete_product_by_id.return_value = None

    result = service.delete_product_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")
    assert result is None
    mock_storage.delete_product_by_id.assert_called_once_with(
        "01JFTE35ZRRZWCSKK6TBB1DZCT"
    )


def test_retrieve_all_products_handles_database_error(mock_storage, service):
    """
    Tests that the `get_all_products` method raises a `DatabaseError`
    when the underlying storage encounters a database issue.
    """
    mock_storage.get_all_products.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        service.get_all_products()

    mock_storage.get_all_products.assert_called_once()


def test_retrieve_product_by_id_handles_value_error(mock_storage, service):
    """
    Tests that the `get_product_by_id` method raises a `ValueError`
    when provided with an invalid product ID.
    """
    mock_storage.get_product_by_id.side_effect = ValueError()

    with pytest.raises(ValueError):
        service.get_product_by_id("01JFTE35")

    mock_storage.get_product_by_id.assert_called_once_with("01JFTE35")


def test_create_product_handles_database_error(product, mock_storage, service):
    """
    Tests that the `create_product` method raises a `DatabaseError`
    when the storage service encounters an issue during product creation.
    """
    mock_storage.create_product.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        service.create_product(product)

    mock_storage.create_product.assert_called_once_with(product)


def test_update_product_handles_value_error(product, mock_storage, service):
    """
    Tests that the `update_product` method raises a `ValueError`
    when the provided product data is invalid.
    """
    mock_storage.update_product.side_effect = ValueError()

    with pytest.raises(ValueError):
        service.update_product(product)

    mock_storage.update_product.assert_called_once_with(product)


def test_delete_product_by_id_handles_value_error(mock_storage, service):
    """
    Tests that the `delete_product_by_id` method raises a `ValueError`
    when provided with an invalid product ID.
    """
    mock_storage.delete_product_by_id.side_effect = ValueError()

    with pytest.raises(ValueError):
        service.delete_product_by_id("01JFTE35")

    mock_storage.delete_product_by_id.assert_called_once_with("01JFTE35")
