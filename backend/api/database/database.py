import pyodbc, struct, bcrypt, urllib
from azure import identity
from typing import List

from sqlalchemy import create_engine, text, event, func, String
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, Session

from azure_keys import AZURE_DRIVER, AZURE_SERVER, AZURE_DATABASE
from table_setup import TABLE_SETUP_QUERY
from market_types import *

Base = declarative_base()

# def database_delete_everything():
#     with conn.cursor() as cursor:
#         cursor.execute(TABLE_SETUP_QUERY)
#         conn.commit()
#         print("Reset database contents")

# def add_product(product: Product) -> int:
#     print("Adding product")

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                         INSERT INTO dbo.Products (Name, Description, Price, OwnerID) 
#                         OUTPUT INSERTED.ID 
#                         VALUES (?, ?, ?, ?)
#                         """, product.name, product.description, product.price, product.owner_id)
#         new_id = cursor.fetchone()[0]
#         print("Successfully added product")
#         conn.commit()
#         return new_id

# def lookup_product(id: int) -> Product:
#     print("Looking up product", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT *
#                        FROM dbo.Products
#                        WHERE ID = ?
#                        """, id)
#         res = cursor.fetchone()
#         if res is None:
#             print("Did not find product", id)
#             return None
#         else:
#             print("Found product", id)
#             product = Product(res.Name, res.Description, res.Price, res.OwnerID)
#             product.set_id(res.ID)
#             return product

# def delete_product(id: int) -> bool:
#     print("Deleting product", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Products
#                        WHERE ID = ?
#                        """, id)
#         product = cursor.fetchone()
#         if product is None:
#             print("Did not find product", id)
#             return False
#         else:
#             cursor.execute("DELETE FROM dbo.Products WHERE ID = ?", id)
#             print("Deleted product", id)
#             conn.commit()
#             return True

# def get_homepage() -> List[Product]:
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT ID, Name, Description, Price, OwnerID 
#                        FROM dbo.Products
#                        """)
#         res = cursor.fetchall()
#         products = []
#         for row in res:
#             product = Product(row[1], row[2], row[3], row[4])
#             product.set_id(row[0])
#             products.append(product)

#         return products

# def search_products(query: str) -> List[Product]:
#     with conn.cursor() as cursor:
#         query = f"%{query.upper()}%"
#         cursor.execute("""
#                        SELECT ID, Name, Description, Price, OwnerID 
#                        FROM dbo.Products
#                        WHERE UPPER(Name) LIKE ? OR
#                        UPPER(Description) LIKE ? ;
#                        """, query, query)
#         res = cursor.fetchall()
#         products = []
#         for row in res:
#             product = Product(row[1], row[2], row[3], row[4])
#             product.set_id(row[0])
#             products.append(product)

#         return products

# def can_register(user: User) -> bool:
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Users 
#                        WHERE Username = ?
#                        OR Email = ?
#                        """, user.username, user.email)
#         res = cursor.fetchone()

#         return res is None

# def add_user(user: User) -> int:
#     print("Adding user " + user.username)

#     if not can_register(user):
#         raise Exception("Failed to register user with username " + user.username)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                         INSERT INTO dbo.Users (Username, Email, Password) 
#                         OUTPUT INSERTED.ID 
#                         VALUES (?, ?, ?)
#                         """, user.username, user.email, user.password)
#         new_id = cursor.fetchone()[0]
#         print("Successfully added user " + user.username)
#         conn.commit()
#         return new_id

# def lookup_user_login(email, password) -> User:
#     print("Looking up user", email)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Users 
#                        WHERE Email = ?
#                        """, email)
#         res = cursor.fetchone()
#         if res is None:
#             print("Did not find user with email", email)
#             return None
        
#         if not bcrypt.checkpw(password.encode('utf-8'), res.Password.encode('utf-8')):
#             print("Found user but credentials were invalid")
#             return None
        
#         print("Found user", email)
#         user = User(res.Username, res.Email, None)
#         user.set_id(res.ID)
#         return user

# def lookup_user(id: int) -> User:
#     print("Looking up user", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Users 
#                        WHERE ID = ?
#                        """, id)
#         res = cursor.fetchone()
#         if res is None:
#             print("Did not find user", id)
#             return None
#         else:
#             print("Found user", id)
#             user = User(res.Username, res.Email, res.Password)
#             user.set_id(res.ID)
#             return user

# def delete_user(id: int) -> bool:
#     print("Deleting user", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Users
#                        WHERE ID = ?
#                        """, id)
#         user = cursor.fetchone()
#         if user is None:
#             print("Did not find user", id)
#             return False
#         else:
#             cursor.execute("DELETE FROM dbo.Users WHERE ID = ?", id)
#             print("Deleted user", id)
#             conn.commit()
#             return True

# def add_message(message: Message) -> int:
#     print("Adding message")

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        INSERT INTO dbo.Messages 
#                        (Title, Content, FromUserID, ToUserID) 
#                        OUTPUT INSERTED.ID
#                        VALUES (?, ?, ?, ?)
#                        """, message.title, message.content, message.from_id, message.to_id)
        
#         print("Message added")
#         new_id = cursor.fetchone()[0]
#         conn.commit()
#         return new_id

# def lookup_message(id: int) -> Message:
#     print("Looking up message", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT *
#                        FROM dbo.Messages
#                        WHERE ID = ?
#                        """, id)
#         res = cursor.fetchone()
#         if res is None:
#             print("Did not find message", id)
#             return None
#         else:
#             print("Found message", id)
#             message = Message(res.ToUserID, res.FromUserID, res.Title, res.Content)
#             message.set_id(res.ID)
#             return message



# def get_messages_to(user_id: int) -> List[Message]:
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT ID, Title, Content, FromUserID, ToUserID
#                        FROM dbo.Messages
#                        WHERE ToUserID = ?
#                        """, user_id)
        
#         res = cursor.fetchall()
#         messages = []
#         for row in res:
#             message = Message(row[4], row[3], row[1], row[2])
#             message.set_id(row[0])
#             messages.append(message)
#         return messages

# def get_messages_from(user_id: int) -> List[Message]:
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT ID, Title, Content, FromUserID, ToUserID
#                        FROM dbo.Messages
#                        WHERE FromUserID = ?
#                        """, user_id)
        
#         res = cursor.fetchall()
#         messages = []
#         for row in res:
#             message = Message(row[4], row[3], row[1], row[2])
#             message.set_id(row[0])
#             messages.append(message)
#         return messages

# def delete_message(id: int) -> bool:
#     print("Deleting message", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT * 
#                        FROM dbo.Messages
#                        WHERE ID = ?
#                        """, id)
#         message = cursor.fetchone()
#         if message is None:
#             print("Did not find message", id)
#             return False
#         else:
#             cursor.execute("DELETE FROM dbo.Messages WHERE ID = ?", id)
#             print("Deleted message", id)
#             conn.commit()
#             return True

# def add_transaction(transaction: Transaction) -> int:
#     print("Adding transaction")

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        INSERT INTO dbo.Transactions
#                        (ProductID, BuyerID) 
#                        OUTPUT INSERTED.ID
#                        VALUES (?, ?)
#                        """, transaction.product_id, transaction.buyer_id)
        
#         print("Transaction added")
#         new_id = cursor.fetchone()[0]
#         conn.commit()
#         return new_id

# def lookup_transaction(id: int) -> Transaction:
#     print("Looking up transaction", id)

#     with conn.cursor() as cursor:
#         cursor.execute("""
#                        SELECT *
#                        FROM dbo.Transactions
#                        WHERE ID = ?
#                        """, id)
#         res = cursor.fetchone()
#         if res is None:
#             print("Did not find transaction", id)
#             return None
#         else:
#             print("Found transaction", id)
#             transaction = Transaction(res.ProductID, res.BuyerID)
#             transaction.set_id(res.ID)
#             return transaction

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    username: Mapped[str] = mapped_column(String(64), name="Username")
    email: Mapped[str] = mapped_column(String(320), name="Email")
    password: Mapped[str] = mapped_column(String(128), name="Password")

    def __repr__(self):
        return f"User(ID={self.id!r} Username={self.username!r} Email={self.email!r}"

class Database:
    def __init__(self):
        self.credential = identity.DefaultAzureCredential()
        self.engine = self._get_engine()
        self.localSession = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Register token provider for SQLAlchemy engine
        @event.listens_for(self.engine, "do_connect")
        def provide_token(_, _2, _3, cparams):
            self._provide_token(cparams)
    
    # Return true if all tables in database are empty.
    def is_empty(self):
        with Session(self.engine) as session:
            query = session.query(func.count('*')).select_from(User)
            return query.scalar() == 0

    def dispose(self):
        self.engine.dispose()
    
    def _get_engine(self):
        connection_string = f"Driver={AZURE_DRIVER};Server=tcp:{AZURE_SERVER}.database.windows.net,1433;Database={AZURE_DATABASE};Encrypt=yes;" + \
            "TrustServerCertificate=no;Connection Timeout=30"
        params = urllib.parse.quote(connection_string)
        url = f"mssql+pyodbc:///?odbc_connect={params}"

        return create_engine(url)
    
    def _provide_token(self, cparams):
        token_bytes = self.credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h

        cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

print(Database().is_empty())
