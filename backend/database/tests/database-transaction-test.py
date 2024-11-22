import pytest
from database import *
from market_types import *

def test_add_transaction():

    id1 = add_user(User("user1", "a@a.com", "pass"))
    id2 = add_user(User("user2", "b@b.com", "pass"))
    prod_id = add_product(Product("chair", "for sitting", 5.5, id1))

    transaction = Transaction(prod_id, id2)
    transaction_id = add_transaction(transaction)

    assert not is_database_empty()

    assert transaction_id == 1
    found_transaction = lookup_transaction(transaction_id)
    assert found_transaction is not None
    assert found_transaction.buyer_id == id2
    assert found_transaction.product_id == prod_id

    assert prod_id == found_transaction.product_id
    found_prod = lookup_product(prod_id)
    assert found_prod is not None
    assert found_prod.id == prod_id
    assert found_prod.name == "chair"
    assert found_prod.description == "for sitting"
    assert found_prod.price == 5.5
    assert found_prod.owner_id == id1

def test_missing_transaction():
    assert lookup_transaction(5) is None
    assert lookup_transaction(50) is None
