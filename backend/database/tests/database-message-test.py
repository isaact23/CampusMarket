import pytest
from database import *
from market_types import *

def test_add_message():
    id1 = add_user(User("user1", "a@a.com", "pass"))
    id2 = add_user(User("user2", "b@b.com", "pass"))

    message_id = add_message(Message(id1, id2, "hello", "how goes it"))

    found_message = lookup_message(message_id)
    assert found_message is not None
    assert found_message.to_id == id1
    assert found_message.from_id == id2
    assert found_message.title == "hello"
    assert found_message.content == "how goes it"

    assert len(get_messages_to(id2)) == 0
    assert len(get_messages_from(id1)) == 0

    assert len(get_messages_to(id1)) == 1
    assert len(get_messages_from(id2)) == 1

def test_delete_message():
    id1 = add_user(User("user1", "a@a.com", "pass"))
    id2 = add_user(User("user2", "b@b.com", "pass"))

    message_id = add_message(Message(id1, id2, "hello", "how goes it"))
    assert delete_message(message_id)
    assert lookup_message(message_id) is None

    assert not delete_message(message_id)
    assert not delete_message(5)
