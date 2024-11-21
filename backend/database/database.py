import pyodbc, struct
from azure import identity
from azure_keys import AZURE_SQL_CONNECTIONSTRING
from table_setup import TABLE_SETUP_QUERY
from market_types import *
from typing import List

def is_database_empty() -> bool:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dbo.Users")
        if cursor.fetchone() is not None:
            return False
        cursor.execute("SELECT * FROM dbo.Products")
        if cursor.fetchone() is not None:
            return False
        cursor.execute("SELECT * FROM dbo.Transactions")
        if cursor.fetchone() is not None:
            return False
        cursor.execute("SELECT * FROM dbo.Messages")
        if cursor.fetchone() is not None:
            return False
        return True

def database_delete_everything():
    with conn.cursor() as cursor:
        cursor.execute(TABLE_SETUP_QUERY)
        conn.commit()
        print("Reset database contents")

def add_product(product: Product) -> int:
    print("Adding product")

    with conn.cursor() as cursor:
        cursor.execute("""
                        INSERT INTO dbo.Products (Name, Description, Price, OwnerID) 
                        OUTPUT INSERTED.ID 
                        VALUES (?, ?, ?, ?)
                        """, product.name, product.description, product.price, product.owner_id)
        new_id = cursor.fetchone()[0]
        print("Successfully added product")
        conn.commit()
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
            conn.commit()
            return True

def get_homepage() -> List[Product]:
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT ID, Name, Description, Price, OwnerID 
                       FROM dbo.Products
                       WHERE ID = ?
                       """, id)
        res = cursor.fetchall()
        products = []
        for row in res:
            product = Product(row[1], row[2], row[3], row[4])
            product.set_id(row[0])
            products.append(product)

        return products

def search_products(query: Query) -> List[Product]:
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT ID, Name, Description, Price, OwnerID 
                       FROM dbo.Products
                       WHERE UPPER(Name) LIKE UPPER('%?%') OR
                       UPPER(Description) LIKE UPPER('%?%')
                       """, id)
        res = cursor.fetchall()
        products = []
        for row in res:
            product = Product(row[1], row[2], row[3], row[4])
            product.set_id(row[0])
            products.append(product)

        return products

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
                           INSERT INTO dbo.Users (Username, Email, Password) 
                           OUTPUT INSERTED.ID 
                           VALUES (?, ?, ?)
                           """, user.username, user.email, user.password)
            new_id = cursor.fetchone()[0]
            print("Successfully added user " + user.username)
            conn.commit()
            return new_id
        else:
            raise Exception("User " + user.username + " already exists.")


def lookup_user(id: int) -> User:
    print("Looking up user", id)

    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM dbo.Users 
                       WHERE ID = ?
                       """, id)
        res = cursor.fetchone()
        if res is None:
            print("Did not find user", id)
            return None
        else:
            print("Found user", id)
            user = User(res.Username, res.Email, res.Password)
            user.set_id(res.ID)
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
            conn.commit()
            return True

def add_message(message: Message) -> int:
    print("Adding message")

    with conn.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO dbo.Messages 
                       (Title, Content, FromUserID, ToUserID) 
                       OUTPUT INSERTED.ID
                       VALUES (?, ?, ?, ?)
                       """, message.title, message.content, message.from_id, message.to_id)
        
        print("Message added")
        new_id = cursor.fetchone()[0]
        conn.commit()
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



def get_messages_to(user_id: int) -> List[Message]:
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT ID, Title, Content, FromUserID, ToUserID
                       FROM dbo.Messages
                       WHERE ToUserID = ?
                       """, user_id)
        
        res = cursor.fetchall()
        messages = []
        for row in res:
            message = Message(row[4], row[3], row[1], row[2])
            message.set_id(row[0])
            messages.append(message)
        return messages

def get_messages_from(user_id: int) -> List[Message]:
    with conn.cursor() as cursor:
        cursor.execute("""
                       SELECT ID, Title, Content, FromUserID, ToUserID
                       FROM dbo.Messages
                       WHERE FromUserID = ?
                       """, user_id)
        
        res = cursor.fetchall()
        messages = []
        for row in res:
            message = Message(row[4], row[3], row[1], row[2])
            message.set_id(row[0])
            messages.append(message)
        return messages

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
            conn.commit()
            return True

def add_transaction(transaction: Transaction) -> int:
    print("Adding transaction")

    with conn.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO dbo.Transactions
                       (ProductID, BuyerID) 
                       OUTPUT INSERTED.ID
                       VALUES (?, ?)
                       """, transaction.product_id, transaction.buyer_id)
        
        print("Transaction added")
        new_id = cursor.fetchone()[0]
        conn.commit()
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
            transaction = Transaction(res.ProductID, res.BuyerID)
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
