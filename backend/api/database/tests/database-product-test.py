import pytest
from database import *
from database_types import *

def test_add_product(database):
    user_id = database.add_user(User("user1", "a@a.com", "pass"))
    prod = Product("chair", "for sitting", 4.50, user_id)
    prod_id = database.add_product(prod)

    assert not database.is_empty()
    
    assert prod_id == 1

    found_prod = database.lookup_product(prod_id)
    assert found_prod is not None
    assert found_prod.id == prod_id
    assert found_prod.name == "chair"
    assert found_prod.description == "for sitting"
    assert found_prod.price == 4.50
    assert found_prod.owner_id == user_id


def test_delete_product(database):
    user_id = database.add_user(User("user1", "a@a.com", "pass"))
    prod = Product("chair", "for sitting", 4.50, user_id)
    prod_id = database.add_product(prod)
    assert database.delete_product(prod_id)
    assert database.lookup_product(prod_id) is None
    
    assert not database.delete_product(prod_id)
    assert not database.delete_product(17)

def test_missing_product(database):
    assert database.lookup_product(5) is None
    assert database.lookup_product(50) is None

def test_search_products(database):
    id1 = database.add_user(User('a', 'a', 'a'))
    id2 = database.add_user(User('b', 'b', 'b'))

    database.add_product(Product('food WOW', 'healthy stuff', 10, id1))
    database.add_product(Product('New Computer', "Has 512kb hard drive and a millibyte of ram", 159.99, id2))
    database.add_product(Product('FREE clothes', 'Select any desired assortment wow', 15.99, id1))
    database.add_product(Product('Shrek rental', 'Watch Shrek in awesome quality 720p resolution wow', 9.99, id2))

    assert len(database.get_homepage()) == 4
    assert len(database.search_products("food")) == 1
    assert len(database.search_products("FOOD")) == 1
    assert len(database.search_products("One of us")) == 0
    assert len(database.search_products("aweSOME")) == 1
    assert len(database.search_products("wow")) == 3
