import pytest
from database import *
from market_types import *

def test_add_user():
    user = User("shuffles", "shuffles@shuffles.shuffles", "shuffles")
    id = add_user(user)

    assert not is_database_empty()

    assert id == 1
    assert lookup_user(id) is not None

    dup_user1 = User("shuffles", "alpha@beta.com", "pass")
    dup_user2 = User("freddy", "shuffles@shuffles.shuffles", "mypass")

    with pytest.raises(Exception):
        add_user(dup_user1)
    with pytest.raises(Exception):
        add_user(dup_user2)


def test_delete_user():
    user = User("user2", "a@a.com", "mypass")
    id = add_user(user)
    delete_user(id)

    assert lookup_user(id) is None

def test_missing_user():
    assert lookup_user(5) is None
    assert lookup_user(50) is None

