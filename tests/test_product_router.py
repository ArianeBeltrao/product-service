from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.product_router import get_product_service


@fixture
def service():
    return MagicMock()


@fixture
def client(service):
    app.dependency_overrides[get_product_service] = lambda: service
    client = TestClient(app)
    return client


@fixture
def product_json():
    return {
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "cacau house",
        "description": "bed for cats",
        "price": 20.0,
        "quantity": 100,
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


def test_router_get_all_products(service, client, product, product_json):
    service.get_all_products.return_value = [product]
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == [product_json]
    service.get_all_products.assert_called_once()


def test_router_get_product_by_id(service, client, product, product_json):
    service.get_product_by_id.return_value = product
    response = client.get("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 200
    assert response.json() == product_json
    service.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_create_product(service, client, product, product_json):
    service.create_product.return_value = product
    response = client.post("/products", json=product_json)

    assert response.status_code == 201
    assert response.json() == product_json
    service.create_product.assert_called_once_with(product)


def test_router_update_product(service, client, product, product_json):
    service.update_product.return_value = product
    response = client.put("/products", json=product_json)

    assert response.status_code == 200
    assert response.json() == product_json
    service.update_product.assert_called_once_with(product)


def test_router_delete_product_by_id(service, client):
    service.delete_product_by_id.return_value = None
    response = client.delete("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 204
    service.delete_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_get_product_by_id_value_error(service, client):
    service.get_product_by_id.side_effect = ValueError()
    response = client.get("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404
    service.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_router_update_product_value_error(service, client, product, product_json):
    service.update_product.side_effect = ValueError()
    response = client.put("/products", json=product_json)

    assert response.status_code == 404
    service.update_product.assert_called_once_with(product)


def test_router_delete_product_by_id_value_error(service, client):
    service.delete_product_by_id.side_effect = ValueError()
    response = client.delete("/products/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404
    service.delete_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")
