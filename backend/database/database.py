import os
import pyodbc, struct
from azure import identity
from azure_keys import AZURE_SQL_CONNECTIONSTRING

from market_types import *
from typing import List

def add_product(product: Product) -> int:

    # INSERT INTO dbo.Users (Username) VALUES ('shuffles');

    with get_conn() as conn:
        cursor = conn.cursor()
        pass # Return Product ID

def lookup_product(id: int) -> Product:
    pass # Return product

def delete_product(id: int) -> bool:
    pass # Return bool

def get_homepage() -> List[Product]:
    pass # Return array of products

def search_products(query: Query) -> List[Product]:
    pass # Return array of products

def add_user(user: User) -> int:
    print("Adding user " + user.username)

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dbo.Users WHERE Username = ?", user.username)
        res = cursor.fetchone()
        if res is None:
            cursor.execute("INSERT INTO dbo.Users (Username) OUTPUT INSERTED.ID VALUES (?)", user.username)
            new_id = cursor.fetchone()[0]
            print("Successfully added user " + user.username)
            return new_id
        else:
            print("User " + user.username + " already exists. Returning their ID")
            return res.ID


def lookup_user(id: int) -> User:
    pass # Return user

def delete_user(id: int) -> bool:
    pass # Return bool

def add_message(message: Message) -> int:
    pass # Return message id

def lookup_message(id: int) -> Message:
    pass

def delete_message(id: int) -> bool:
    pass

def add_transaction(transaction: Transaction) -> int:
    pass

def lookup_transaction(id: int) -> Transaction:
    pass

def get_conn():
    cred = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = cred.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

print("Authenticating into database")
conn = get_conn()
print("Authenticated into database")

print(add_user(User(0, "Randy")))