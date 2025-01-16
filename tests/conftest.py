from datetime import datetime

from pytest import fixture

from models.product import Product


@fixture(name="product")
def fixture_product():
    """
    Creates a sample Product instance for testing purposes.

    Returns:
        Product: A Product instance with predefined attributes.
    """
    return Product(
        id="01JFTE35ZRRZWCSKK6TBB1DZCT",
        name="house",
        description="bed for cats",
        price=20.0,
        quantity=100,
        active=True,
        created_at=datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at=None,
    )
