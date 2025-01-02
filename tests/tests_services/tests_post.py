import pytest
from fastapi.testclient import TestClient
from main import app
from models.product import Product
from unittest.mock import MagicMock

client = TestClient(app)

@pytest.fixture
def mock_product_service(monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr("main.ProductService", mock_service)
    return mock_service

def test_create_product(mock_product_service):
    product_data = {
        "id": "1",
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "quantity": 100,
        "active": True,
        "created_at": None,
        "updated_at": None
    }
    product = Product(**product_data)
    mock_product_service.create_product.return_value = product

    response = client.post("/products", json=product_data)

    assert response.status_code == 200
    assert response.json() == product_data
    mock_product_service.create_product.assert_called_once_with(product)
