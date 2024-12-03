import pytest
import sys
import os

# Add the project root to sys.path to resolve the 'api' module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from api.database import database_types
from api.database.database import Database

db = Database()

# Sample fixture to initialize the database and clean up after tests
@pytest.fixture(scope="module")
def init_db():
    # Set up the database (e.g., create tables, seed data)
    db.reset()
    yield
    # Tear down the database (e.g., drop tables)
    db.reset()

# Helper function to compare object attributes
def assert_user_equal(user1, user2):
    assert user1.username == user2.username
    assert user1.email == user2.email
    assert user1.password == user2.password

def assert_product_equal(product1, product2):
    assert product1.name == product2.name
    assert product1.description == product2.description
    assert product1.price == product2.price
    assert product1.owner_id == product2.owner_id

def assert_transaction_equal(transaction1, transaction2):
    assert transaction1.product_id == transaction2.product_id
    assert transaction1.buyer_id == transaction2.buyer_id

def assert_message_equal(message1, message2):
    assert message1.title == message2.title
    assert message1.content == message2.content
    assert message1.from_user_id == message2.from_user_id
    assert message1.to_user_id == message2.to_user_id

# Integration test to validate interaction between user and product-related functions
def test_user_and_product_interaction(init_db):
    # Create a user and add them to the database
    user = database_types.User(username="Test User", email="testuser@example.com", password="password123")
    db.add_user(user)

    # Verify the user exists in the database
    retrieved_user = db.lookup_user(user.id)
    assert_user_equal(retrieved_user, user)

    # Create a product and add it to the database
    product = database_types.Product(name="Test Product", description="A sample product", price=10.0, owner_id=user.id)
    db.add_product(product)

    # Verify the product exists in the database and belongs to the user
    retrieved_product = db.lookup_product(product.id)
    assert_product_equal(retrieved_product, product)

# Integration test to validate transaction between users
def test_transaction_between_users(init_db):
    # Create two users
    user1 = database_types.User(username="User One", email="userone@example.com", password="password123")
    user2 = database_types.User(username="User Two", email="usertwo@example.com", password="password123")
    db.add_user(user1)
    db.add_user(user2)

    # Create a product owned by user1
    product = database_types.Product(name="User One's Product", description="A product by User One", price=15.0, owner_id=user1.id)
    db.add_product(product)

    # Perform a transaction where user2 buys the product from user1
    transaction = database_types.Transaction(product_id=product.id, buyer_id=user2.id)
    db.add_transaction(transaction)

    # Update the product's ownership to user2 after the transaction
    product.owner_id = user2.id
    db.add_product(product)  # Update the product in the database

    # Verify the transaction exists in the database
    retrieved_transaction = db.lookup_transaction(transaction.id)
    assert_transaction_equal(retrieved_transaction, transaction)

    # Verify that the product ownership has been transferred to user2
    updated_product = db.lookup_product(product.id)
    assert updated_product.owner_id == user2.id

# Integration test to validate interactions between messages and users
def test_message_exchange(init_db):
    # Create two users
    user1 = database_types.User(username="User A", email="usera@example.com", password="password123")
    user2 = database_types.User(username="User B", email="userb@example.com", password="password123")
    db.add_user(user1)
    db.add_user(user2)

    # User1 sends a message to User2
    message = database_types.Message(title="Hello", content="Hello, User B!", from_user_id=user1.id, to_user_id=user2.id)
    db.add_message(message)

    # Verify the message exists in the database
    retrieved_message = db.lookup_message(message.id)
    assert_message_equal(retrieved_message, message)

# Test user registration when user already exists
def test_user_registration_duplicate(init_db):
    user = database_types.User(username="ExistingUser", email="existing@example.com", password="password123")
    db.add_user(user)

    # Attempt to register the same user again
    can_register = db.can_register(user)
    assert can_register is False

# Test deletion of users, products, and messages
def test_deletion_methods(init_db):
    # Create a user and add them to the database
    user = database_types.User(username="DeleteUser", email="deleteuser@example.com", password="password123")
    db.add_user(user)

    # Delete the user
    deleted = db.delete_user(user.id)
    assert deleted is True

    # Attempt to delete a non-existing user
    deleted_again = db.delete_user(user.id)
    assert deleted_again is False

# Test if the database is empty after reset
def test_is_empty(init_db):
    # Ensure the database is reset properly before checking if it's empty
    db.reset()
    is_empty = db.is_empty()
    assert is_empty is True

    # Add a user and check again
    user = database_types.User(username="NonEmptyUser", email="nonempty@example.com", password="password123")
    db.add_user(user)
    is_empty = db.is_empty()
    assert is_empty is False

if __name__ == "__main__":
    pytest.main(["api/integration_tests/integration_tests.py"])
