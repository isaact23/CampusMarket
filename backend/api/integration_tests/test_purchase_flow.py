import pytest
from api.database.database_types import User, Product, Transaction

def test_purchase_flow(database):
    # Setup users
    seller_id = database.add_user(User("seller", "seller@gmu.edu", "pass123"))
    buyer_id = database.add_user(User("buyer", "buyer@gmu.edu", "pass123"))
    
    # Create product
    product = Product("Calculator", "TI-84", 50.00, seller_id)
    product_id = database.add_product(product)
    
    # Create transaction
    transaction = Transaction(product_id, buyer_id)
    transaction_id = database.add_transaction(transaction)
    
    # Verify transaction
    found_transaction = database.lookup_transaction(transaction_id)
    assert found_transaction is not None
    assert found_transaction.buyer_id == buyer_id
    assert found_transaction.product_id == product_id 