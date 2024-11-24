import pytest
from database import *
from market_types import *

def test_add_user():
    user = User("shuffles", "shuffles@shuffles.shuffles", "shuffles2")
    id = add_user(user)

    assert not is_database_empty()

    assert id == 1
    found_user = lookup_user(id)
    assert found_user is not None
    assert found_user.id == 1
    assert found_user.username == "shuffles"
    assert found_user.email == "shuffles@shuffles.shuffles"
    assert found_user.password == "shuffles2"

    dup_user1 = User("shuffles", "alpha@beta.com", "pass")
    dup_user2 = User("freddy", "shuffles@shuffles.shuffles", "mypass")

    with pytest.raises(Exception):
        add_user(dup_user1)
    with pytest.raises(Exception):
        add_user(dup_user2)


def test_delete_user():
    user = User("user2", "a@a.com", "mypass")
    id = add_user(user)
    assert delete_user(id)
    assert lookup_user(id) is None

    assert not delete_user(id)
    assert not delete_user(20)

    

def test_missing_user():
    assert lookup_user(5) is None
    assert lookup_user(50) is None