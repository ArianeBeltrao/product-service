import unittest
from unittest.mock import MagicMock
from services.product_service import ProductService
from models.product import Product
from storages.product_storage import ProductStorage
from datetime import datetime

class TestProductService(unittest.TestCase):

    def setUp(self):
        self.storage = MagicMock(ProductStorage)
        self.service = ProductService(self.storage)

    def test_create_product(self):
        product = Product(
            name="Test Product",
            description="Test Description",
            price=10.0,
            quantity=100,
            created_at=datetime.now()
        )
        self.storage.save_product.return_value = product

        result = self.service.create_product(product)

        self.storage.save_product.assert_called_once_with(product)
        self.assertEqual(result, product)
        
    def test_create_product_with_invalid_name(self):
        product = Product(
            name="",
            description="Test Description",
            price=10.0,
            quantity=100,
            created_at=datetime.now()
        )

        with self.assertRaises(ValueError) as context:
            self.service.create_product(product)

        self.assertEqual(str(context.exception), "Product name cannot be empty")




