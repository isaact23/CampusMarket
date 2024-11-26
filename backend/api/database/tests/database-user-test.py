import pytest
from database import *
from database_types import *

def test_add_user(database):
    user = User("shuffles", "shuffles@shuffles.shuffles", "shuffles2")
    id = database.add_user(user)

    assert not database.is_empty()

    assert id == 1
    found_user = database.lookup_user(id)
    assert found_user is not None
    assert found_user.id == 1
    assert found_user.username == "shuffles"
    assert found_user.email == "shuffles@shuffles.shuffles"
    assert found_user.password == "shuffles2"

    dup_user1 = User("shuffles", "alpha@beta.com", "pass")
    dup_user2 = User("freddy", "shuffles@shuffles.shuffles", "mypass")

    with pytest.raises(Exception):
        database.add_user(dup_user1)
    with pytest.raises(Exception):
        database.add_user(dup_user2)


def test_delete_user(database):
    user = User("user2", "a@a.com", "mypass")
    id = database.add_user(user)
    assert database.delete_user(id)
    assert database.lookup_user(id) is None

    assert not database.delete_user(id)
    assert not database.delete_user(20)

    

def test_missing_user(database):
    assert database.lookup_user(5) is None
    assert database.lookup_user(50) is None
