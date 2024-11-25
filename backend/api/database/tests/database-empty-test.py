import pytest
from database_types import *

def test_messages(database):
    assert database.is_empty()

    database.add_user(User('a', 'a', 'a'))
    assert not database.is_empty()

    id1 = database.add_user(User("user1", "a@a.com", "pass")) # To
    id2 = database.add_user(User("user2", "b@b.com", "pass")) # From

    message_id = database.add_message(Message("hello", "how goes it", id2, id1))

    found_message = database.lookup_message(message_id)
    assert found_message is not None
    assert found_message.to_user_id == id1
    assert found_message.from_user_id == id2
    assert found_message.title == "hello"
    assert found_message.content == "how goes it"

    assert len(database.get_messages_to(id2)) == 0
    assert len(database.get_messages_from(id1)) == 0

    assert len(database.get_messages_to(id1)) == 1
    assert len(database.get_messages_from(id2)) == 1
