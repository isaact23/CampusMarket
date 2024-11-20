import pytest
from database import *
from market_types import *

@pytest.fixture(scope="module")
def setup():
    print("Test")
    print("Here: Ensure that all tables are empty")

def test_add_user():
    user = User("shuffles", "shuffles@shuffles.shuffles", "shuffles")
    id = add_user(user)

    assert id == 1
    assert lookup_user(id) is not None

def test_delete_user():
    user = User("user2", "a@a.com", "mypass")
    id = add_user(user)
    delete_user(id)

    assert lookup_user(id) is None
