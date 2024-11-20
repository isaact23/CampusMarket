import pytest
from database import add_product, lookup_product, delete_product
from market_types import *

@pytest.fixture(scope="module")
def setup():
    print("Test")
    print("Here: Ensure that all tables are empty")

def test_add_product_integration():
    product = Product("Test Product", "Description", 10, 1)
    new_id = add_product(product)

    # Assert the product is added to the database
    assert new_id == 1
    assert lookup_product(new_id) is not None

def test_delete_product_integration():
    product = Product("Another Product", "Description", 20, 2)
    new_id = add_product(product)
    delete_product(id)

    assert lookup_product(id) is None