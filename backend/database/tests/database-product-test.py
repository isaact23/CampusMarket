import pytest
from database import *
from market_types import *

def test_add_product():
    user_id = add_user(User("user1", "a@a.com", "pass"))
    prod = Product("chair", "for sitting", 4.50, user_id)
    prod_id = add_product(prod)

    assert not is_database_empty()
    
    assert prod_id == 1

    found_prod = lookup_product()
    assert found_prod is not None
    assert found_prod.id == prod_id
    assert found_prod.name == "chair"
    assert found_prod.description == "for sitting"
    assert found_prod.price == 4.50
    assert found_prod.user_id == user_id


def test_delete_product():
    user_id = add_user(User("user1", "a@a.com", "pass"))
    prod = Product("chair", "for sitting", 4.50, user_id)
    prod_id = add_product(prod)
    delete_product(prod_id)
    assert lookup_product(prod_id) is None

def test_missing_product():
    assert lookup_product(5) is None
    assert lookup_product(50) is None
