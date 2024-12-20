# TODO: Re-write queries to be more efficient

import bcrypt, urllib, os, logging
from azure import identity
from typing import List

from sqlalchemy import create_engine, event, func, or_, select
from sqlalchemy.orm import sessionmaker, Session

from .database_types import TypeBase, User, Product, Transaction, Message

AZURE_DRIVER="{ODBC Driver 18 for SQL Server}"
AZURE_SERVER="campusmarket-serv"
AZURE_DATABASE="market-database"
AZURE_USERNAME="ithomps3"

AZURE_PASSWORD = os.environ['AZURE_PASSWORD']

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.credential = identity.DefaultAzureCredential()
        self.engine = self._get_engine()
        self.localSession = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.debug("Got to the end of init")
    
    # Get a list of products to display on the homepage.
    def get_homepage(self) -> List[Product]:
        with Session(self.engine) as session:
            stmt = select(Product)
            return session.scalars(stmt).all()

    # Search products by comparing a query string to the name and descriptions
    # of products.
    def search_products(self, query: str) -> List[Product]:
        with Session(self.engine) as session:
            queryStr = f'%{query}%'
            stmt = select(Product).filter(
                or_(
                    Product.name.ilike(queryStr),
                    Product.description.ilike(queryStr)
                )
            )
            return session.scalars(stmt).all()

    # If the email and password correspond to a valid user, return the User
    # (indicating login allowed), otherwise return None (login rejected).
    def can_login(self, email, password) -> User:
        logging.debug("can_login")
        with Session(self.engine) as session:
            stmt = select(User).where(User.email == email)
            user = session.scalars(stmt).first()
            if user is None:
                return None
            hashword = user.password
            if bcrypt.checkpw(password.encode('utf-8'), hashword.encode('utf-8')):
                return user
            else:
                return None

    # If the email or username is already taken, return False.
    # Otherwise, return True, indicating that the user is allowed to register.
    def can_register(self, user: User) -> bool:
        with Session(self.engine) as session:
            query = session.query(func.count('*')).select_from(User).where(
                or_(
                    User.username == user.username, 
                    User.email == user.email
                )
            )
            return query.scalar() == 0

    # Add a new user. Throws an exception if the user cannot be registered.
    def add_user(self, user: User) -> int:
        if not self.can_register(user):
            raise Exception("Failed to add user (conflicting username or email)")

        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            return user.id

    # Lookup a user by ID. Return the User if found or None if not found.
    def lookup_user(self, id: int) -> User:
        with Session(self.engine) as session:
            stmt = select(User).where(User.id == id)
            for user in session.scalars(stmt):
                return user
            return None

    # Delete a user by ID. Return True if successfully deleted.
    def delete_user(self, id: int) -> bool:
        with Session(self.engine) as session:
            user = self.lookup_user(id)
            if user is None:
                return False
            
            session.delete(user)
            session.commit()
            return True
    
    # Add a product to the database and return its ID.
    def add_product(self, product: Product) -> int:
        with Session(self.engine) as session:
            session.add(product)
            session.commit()
            return product.id

    # Find a product by ID. Returns the Product if found or None if not found.
    def lookup_product(self, id: int) -> Product:
        with Session(self.engine) as session:
            stmt = select(Product).where(Product.id == id)
            for product in session.scalars(stmt):
                return product
            return None
    
    # List products by Owner ID.
    def list_products(self, owner_id: int) -> List[Product]:
        with Session(self.engine) as session:
            stmt = select(Product).filter(
                Product.owner_id == owner_id
            )
            return session.scalars(stmt).all()

    # Delete a product by ID. Returns True if successfully deleted.
    def delete_product(self, id: int) -> bool:
        with Session(self.engine) as session:
            product = self.lookup_product(id)
            if product is None:
                return False
            
            session.delete(product)
            session.commit()
            return True

    # Get all messages sent to a user specified by ID.
    def get_messages_to(self, user_id: int) -> List[Message]:
        with Session(self.engine) as session:
            stmt = select(Message).where(Message.to_user_id == user_id)
            return session.scalars(stmt).all()

    # Get all messages sent from a user specified by ID.
    def get_messages_from(self, user_id: int) -> List[Message]:
        with Session(self.engine) as session:
            stmt = select(Message).where(Message.from_user_id == user_id)
            return session.scalars(stmt).all()

    # Add a message to the database and return its ID.
    def add_message(self, message: Message) -> int:
        with Session(self.engine) as session:
            session.add(message)
            session.commit()
            return message.id

    # Lookup a message by ID. Returns the Message if found or None if not found.
    def lookup_message(self, id: int) -> Message:
        with Session(self.engine) as session:
            stmt = select(Message).where(Message.id == id)
            for message in session.scalars(stmt):
                return message
            return None


    # Delete a message by ID. Returns True if successfully deletee.
    def delete_message(self, id: int) -> bool:
        with Session(self.engine) as session:
            message = self.lookup_message(id)
            if message is None:
                return False
            
            session.delete(message)
            session.commit()
            return True

    # Get all transactions for a buyer user ID.
    def get_transactions_from_buyer(self, user_id: int) -> List[Transaction]:
        with Session(self.engine) as session:
            stmt = select(Transaction).where(Transaction.buyer_id == user_id)
            return session.scalars(stmt).all()

    # Add a transaction to the database and return its ID.
    def add_transaction(self, transaction: Transaction) -> int:
        with Session(self.engine) as session:
            session.add(transaction)
            session.commit()
            return transaction.id

    # Lookup a transaction by ID. Return the Transaction if found or None if not found.
    def lookup_transaction(self, id: int) -> Transaction:
        with Session(self.engine) as session:
            stmt = select(Transaction).where(Transaction.id == id)
            for transaction in session.scalars(stmt):
                return transaction
            return None
    
    # Return true if all tables in database are empty.
    def is_empty(self):
        with Session(self.engine) as session:
            query = session.query(func.count('*')).select_from(User)
            return query.scalar() == 0
    
    # Reset all tables in the database.
    def reset(self):
        TypeBase.metadata.drop_all(self.engine)
        TypeBase.metadata.create_all(self.engine)

    def dispose(self):
        self.engine.dispose()
    
    def _get_engine(self):
        try:
            connection_string = f"DRIVER={AZURE_DRIVER};SERVER=tcp:campusmarket-serv.database.windows.net,1433;DATABASE={AZURE_DATABASE};" + \
                f"UID={AZURE_USERNAME};PWD={AZURE_PASSWORD}"
            params = urllib.parse.quote(connection_string)
            url = f"mssql+pyodbc:///?odbc_connect={params}"
        except:
            logger.error("Something went wrong while initializing the database.")

        return create_engine(url)
