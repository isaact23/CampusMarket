import pytest
import sys
import os
import bcrypt

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

# Test to validate the homepage product retrieval
def test_get_homepage(init_db):
    # Create a user for product ownership
    user = database_types.User(username="HomepageOwner", email="homepageowner@example.com", password="password123")
    if db.can_register(user):
        db.add_user(user)

    # Refresh user to get assigned ID
    user = db.lookup_user(user.id)
    assert user is not None

    # Add products to the database
    product1 = database_types.Product(name="Homepage Product 1", description="Description 1", price=20.0, owner_id=user.id)
    product2 = database_types.Product(name="Homepage Product 2", description="Description 2", price=25.0, owner_id=user.id)
    db.add_product(product1)
    db.add_product(product2)

    # Get the homepage products
    products = db.get_homepage()
    assert len(products) >= 2  # At least the two products we added should be present

# Test to validate product search
def test_search_products(init_db):
    # Create a user for product ownership
    user = database_types.User(username="SearchOwner", email="searchowner@example.com", password="password123")
    if db.can_register(user):
        db.add_user(user)

    # Refresh user to get assigned ID
    user = db.lookup_user(user.id)
    assert user is not None

    # Add products to the database
    product1 = database_types.Product(name="Search Product 1", description="Unique description", price=30.0, owner_id=user.id)
    product2 = database_types.Product(name="Another Product", description="Different description", price=35.0, owner_id=user.id)
    db.add_product(product1)
    db.add_product(product2)

    # Search for a product by a unique term
    results = db.search_products("Unique")
    assert len(results) == 1
    assert_product_equal(results[0], product1)

# Test to validate user login
def test_can_login(init_db):
    # Create a user and add to the database
    password = "securepassword"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = database_types.User(username="LoginUser", email="loginuser@example.com", password=hashed_password)
    if db.can_register(user):
        db.add_user(user)

    # Test correct login
    logged_in_user = db.can_login(email="loginuser@example.com", password=password)
    assert logged_in_user is not None
    assert_user_equal(logged_in_user, user)

    # Test incorrect login
    logged_in_user = db.can_login(email="loginuser@example.com", password="wrongpassword")
    assert logged_in_user is None

# Test to validate getting messages from a specific user
def test_get_messages_from(init_db):
    # Create users
    user1 = database_types.User(username="UserTo", email="userto@example.com", password="password123")
    user2 = database_types.User(username="UserFrom", email="userfrom@example.com", password="password123")
    if db.can_register(user1):
        db.add_user(user1)
    if db.can_register(user2):
        db.add_user(user2)

    # Refresh users to get assigned IDs
    user1 = db.lookup_user(user1.id)
    user2 = db.lookup_user(user2.id)
    assert user1 is not None
    assert user2 is not None

    # User2 sends a message to User1
    message = database_types.Message(title="Hello", content="Hello, UserTo!", from_user_id=user2.id, to_user_id=user1.id)
    db.add_message(message)

    # Verify the message exists in the database from User2
    messages_from_user2 = db.get_messages_from(user2.id)
    assert len(messages_from_user2) == 1
    assert_message_equal(messages_from_user2[0], message)

# Test to validate transactions from a buyer
def test_get_transactions_from_buyer(init_db):
    # Create users and product
    user1 = database_types.User(username="Buyer", email="buyer@example.com", password="password123")
    user2 = database_types.User(username="Seller", email="seller@example.com", password="password123")
    if db.can_register(user1):
        db.add_user(user1)
    if db.can_register(user2):
        db.add_user(user2)

    # Refresh users to get assigned IDs
    user1 = db.lookup_user(user1.id)
    user2 = db.lookup_user(user2.id)
    assert user1 is not None
    assert user2 is not None

    product = database_types.Product(name="Product to Buy", description="Description", price=50.0, owner_id=user2.id)
    db.add_product(product)

    # User1 buys the product from User2
    transaction = database_types.Transaction(product_id=product.id, buyer_id=user1.id)
    db.add_transaction(transaction)

    # Verify the transaction exists in the database for User1
    transactions = db.get_transactions_from_buyer(user1.id)
    assert len(transactions) == 1
    assert_transaction_equal(transactions[0], transaction)

# Test to validate deleting a product
def test_delete_product(init_db):
    # Create a user for product ownership
    user = database_types.User(username="ProductOwner", email="productowner@example.com", password="password123")
    if db.can_register(user):
        db.add_user(user)

    # Refresh user to get assigned ID
    user = db.lookup_user(user.id)
    assert user is not None

    # Add a product to the database
    product = database_types.Product(name="Product to Delete", description="Description", price=40.0, owner_id=user.id)
    product_id = db.add_product(product)

    # Verify the product was added
    added_product = db.lookup_product(product_id)
    assert added_product is not None
    assert_product_equal(added_product, product)

    # Delete the product
    deletion_successful = db.delete_product(product_id)
    assert deletion_successful is True

    # Verify the product no longer exists
    deleted_product = db.lookup_product(product_id)
    assert deleted_product is None

if __name__ == "__main__":
    pytest.main(["api/integration_tests/integration_tests.py"])
