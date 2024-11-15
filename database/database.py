import pyodbc, struct
from azure import identity
from azure_keys import AZURE_SQL_CONNECTIONSTRING

from market_types import *
from typing import List

def add_product(product: Product) -> int:
    print("Adding product")

    with conn.cursor() as cursor:
        cursor.execute("""
                        INSERT INTO dbo.Products (Name, Description, Price, OwnerID) 
                        OUTPUT INSERTED.ID 
                        VALUES (? ? ? ?)
                        """, product.name, product.description, product.price, product.owner_id)
        new_id = cursor.fetchone()[0]
        print("Successfully added product")
        return new_id

def lookup_product(id: int) -> Product:
    print("Looking up product", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT *
                       FROM dbo.Products
                       WHERE ID = ?
                       """, id)
        res = cursor.fetchone()
        if res is None:
            print("Did not find product", id)
            return None
        else:
            print("Found product", id)
            product = Product(res.Name, res.Description, res.Price, res.OwnerID)
            product.set_id(res.ID)
            return product

def delete_product(id: int) -> bool:
    print("Deleting product", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Products
                       WHERE ID = ?
                       """, id)
        product = cursor.fetchone()
        if product is None:
            print("Did not find product", id)
            return False
        else:
            cursor.execute("DELETE FROM dbo.Products WHERE ID = ?", id)
            print("Deleted product", id)
            return True

def get_homepage() -> List[Product]:
    pass # Return array of products

def search_products(query: Query) -> List[Product]:
    pass # Return array of products

def add_user(user: User) -> int:
    print("Adding user " + user.username)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Users 
                       WHERE Username = ?
                       """, user.username)
        res = cursor.fetchone()
        if res is None:
            cursor.execute("""
                           INSERT INTO dbo.Users (Username) 
                           OUTPUT INSERTED.ID 
                           VALUES (?)
                           """, user.username)
            new_id = cursor.fetchone()[0]
            print("Successfully added user " + user.username)
            return new_id
        else:
            print("User " + user.username + " already exists. Returning their ID")
            return res.ID


def lookup_user(id: int) -> User:
    print("Looking up user", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Users 
                       WHERE ID = ?
                       """, id)
        user = cursor.fetchone()
        if user is None:
            print("Did not find user", id)
            return None
        else:
            print("Found user", id)
            user = User(user.Username)
            user.set_id(user.ID)
            return user

def delete_user(id: int) -> bool:
    print("Deleting user", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Users
                       WHERE ID = ?
                       """, id)
        user = cursor.fetchone()
        if user is None:
            print("Did not find user", id)
            return False
        else:
            cursor.execute("DELETE FROM dbo.Users WHERE ID = ?", id)
            print("Deleted user", id)
            return True

def add_message(message: Message) -> int:
    print("Adding message")

    with conn.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO dbo.Messages 
                       (Title, Content, FromUserID, ToUserID) 
                       OUTPUT INSERTED.ID
                       VALUES (? ? ? ?)
                       """, message.title, message.content, message.from_id, message.to_id)
        
        print("Message added")
        new_id = cursor.fetchone()[0]
        return new_id

def lookup_message(id: int) -> Message:
    print("Looking up message", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT *
                       FROM dbo.Messages
                       WHERE ID = ?
                       """, id)
        res = cursor.fetchone()
        if res is None:
            print("Did not find message", id)
            return None
        else:
            print("Found message", id)
            message = Message(res.ToUserID, res.FromUserID, res.Title, res.Content)
            message.set_id(res.ID)
            return message

def delete_message(id: int) -> bool:
    print("Deleting message", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Messages
                       WHERE ID = ?
                       """, id)
        message = cursor.fetchone()
        if message is None:
            print("Did not find message", id)
            return False
        else:
            cursor.execute("DELETE FROM dbo.Messages WHERE ID = ?", id)
            print("Deleted message", id)
            return True

def add_transaction(transaction: Transaction) -> int:
    print("Adding transaction")

    with conn.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO dbo.Transactions
                       (ProductID, BuyingUserID, SellingUserID) 
                       OUTPUT INSERTED.ID
                       VALUES (? ? ?)
                       """, transaction.product_id, transaction.buying_user_id, transaction.selling_user_id)
        
        print("Transaction added")
        new_id = cursor.fetchone()[0]
        return new_id

def lookup_transaction(id: int) -> Transaction:
    print("Looking up transaction", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT *
                       FROM dbo.Transactions
                       WHERE ID = ?
                       """, id)
        res = cursor.fetchone()
        if res is None:
            print("Did not find transaction", id)
            return None
        else:
            print("Found transaction", id)
            transaction = Transaction(res.ProductID, res.BuyingUserID, res.SellingUserID)
            transaction.set_id(res.ID)
            return transaction

def get_conn():
    cred = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = cred.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256

    try:
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        return conn
    
    except pyodbc.OperationalError:
        raise RuntimeError("Failed to connect to Azure")

print("Authenticating into database")
conn = get_conn()
print("Authenticated into database")

print(add_user(User("shuffles")))