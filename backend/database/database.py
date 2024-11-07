import os
import pyodbc, struct
from azure import identity
from azure_keys import AZURE_SQL_CONNECTIONSTRING

from market_types import *
from typing import List

def add_product(product: Product) -> int:
    with get_conn() as conn:
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
    pass # Return User ID

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

get_conn()