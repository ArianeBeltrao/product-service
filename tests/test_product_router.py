from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.product_router import get_product_service


@fixture(name="service")
def fixture_service():
    """
    Creates a mock service object to simulate the product service layer.

    Returns:
        MagicMock: A mock service object.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    """
    Creates a TestClient instance with a mock product service dependency.

    This fixture overrides the `get_product_service` dependency in the app
    with the mock service, enabling testing of API endpoints.

    Args:
        service (MagicMock): A mock service object.

    Returns:
        TestClient: A TestClient instance for testing the FastAPI application.
    """
    app.dependency_overrides[get_product_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="product_json")
def fixture_product_json():
    return {
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "house",
        "description": "bed for cats",
        "price": 20.0,
        "quantity": 100,
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


def test_router_get_all_products(service, client, product, product_json):
    """
    Tests the GET /products endpoint for retrieving all products.

    Verifies:
    - Response status code is 200.
    - Response JSON matches the mocked product list.
    - Service method `get_all_products` is called once.
    """
    service.get_all_products.return_value = [product]
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == [product_json]
    service.get_all_products.assert_called_once()


def test_router_get_product_by_id(service, client, product, product_json):
    """
    Tests the GET /products/{id} endpoint for retrieving a product by ID.

    Verifies:
    - Response status code is 200.
    - Response JSON matches the mocked product.
    - Service method `get_product_by_id` is called with the correct ID.
    """
    service.get_product_by_id.return_value = product
    response = client.get("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 200
    assert response.json() == product_json
    service.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_get_product_by_name(service, client, product, product_json):
    """
    Tests the GET /products/name/{name} endpoint for retrieving a product by name.

    Verifies:
    - Response status code is 200.
    - Response JSON matches the mocked product.
    - Service method `get_product_by_name` is called with the correct name.
    """
    service.get_product_by_name.return_value = product
    response = client.get("/products/name/house")

    assert response.status_code == 200
    assert response.json() == product_json
    service.get_product_by_name.assert_called_once_with("house")


def test_router_create_product(service, client, product, product_json):
    """
    Tests the POST /products endpoint for creating a new product.

    Verifies:
    - Response status code is 201.
    - Response JSON matches the mocked created product.
    - Service method `create_product` is called with the correct product data.
    """
    service.create_product.return_value = product
    response = client.post("/products", json=product_json)

    assert response.status_code == 201
    assert response.json() == product_json
    service.create_product.assert_called_once_with(product)


def test_router_update_product(service, client, product, product_json):
    """
    Tests the PUT /products endpoint for updating an existing product.

    Verifies:
    - Response status code is 200.
    - Response JSON matches the mocked updated product.
    - Service method `update_product` is called with the correct product data.
    """
    service.update_product.return_value = product
    response = client.put("/products", json=product_json)

    assert response.status_code == 200
    assert response.json() == product_json
    service.update_product.assert_called_once_with(product)


def test_router_delete_product_by_id(service, client):
    """
    Tests the DELETE /products/{id} endpoint for deleting a product by ID.

    Verifies:
    - Response status code is 204.
    - Service method `delete_product_by_id` is called with the correct ID.
    """
    service.delete_product_by_id.return_value = None
    response = client.delete("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 204
    service.delete_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_get_product_by_id_value_error(service, client):
    """
    Tests the GET /products/{id} endpoint when a ValueError is raised.

    Verifies:
    - Response status code is 404.
    - Service method `get_product_by_id` is called with the correct ID.
    """
    service.get_product_by_id.side_effect = ValueError()
    response = client.get("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404
    service.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_get_product_by_name_value_error(service, client):
    """
    Tests the GET /products/name/{name} endpoint when a ValueError is raised.

    Verifies:
    - Response status code is 404.
    - Service method `get_product_by_name` is called with the correct name.
    """
    service.get_product_by_name.side_effect = ValueError()
    response = client.get("/products/name/house")

    assert response.status_code == 404
    service.get_product_by_name.assert_called_once_with("house")


def test_router_update_product_value_error(service, client, product, product_json):
    """
    Tests the PUT /products endpoint when a ValueError is raised during update.

    Verifies:
    - Response status code is 404.
    - Service method `update_product` is called with the correct product data.
    """
    service.update_product.side_effect = ValueError()
    response = client.put("/products", json=product_json)

    assert response.status_code == 404
    service.update_product.assert_called_once_with(product)


def test_router_delete_product_by_id_value_error(service, client):
    """
    Tests the DELETE /products/{id} endpoint when a ValueError is raised.

    Verifies:
    - Response status code is 404.
    - Service method `delete_product_by_id` is called with the correct ID.
    """
    service.delete_product_by_id.side_effect = ValueError()
    response = client.delete("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404
    service.delete_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")
