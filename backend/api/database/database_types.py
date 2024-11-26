from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

TypeBase = declarative_base()

class User(TypeBase):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    username: Mapped[str] = mapped_column(String(64), name="Username")
    email: Mapped[str] = mapped_column(String(320), name="Email")
    password: Mapped[str] = mapped_column(String(128), name="Password")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(ID={self.id!r} Username={self.username!r} Email={self.email!r} Password={self.password!r})"

class Product(TypeBase):
    __tablename__ = "Products"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    name: Mapped[str] = mapped_column(String(100), name="Name")
    description: Mapped[str] = mapped_column(String(1000), name="Description")
    price: Mapped[float] = mapped_column(Numeric(10, 2), name="Price")
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.ID"), name="OwnerID")

    def __init__(self, name, description, price, owner_id):
        self.name = name
        self.description = description
        self.price = price
        self.owner_id = owner_id

class Transaction(TypeBase):
    __tablename__ = "Transactions"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    product_id: Mapped[int] = mapped_column(ForeignKey("Products.ID"), name="ProductID")
    buyer_id: Mapped[int] = mapped_column(ForeignKey("Users.ID"), name="BuyerID")

    def __init__(self, product_id, buyer_id):
        self.product_id = product_id
        self.buyer_id = buyer_id

class Message(TypeBase):
    __tablename__ = "Messages"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    title: Mapped[str] = mapped_column(String(100), name="Title")
    content: Mapped[str] = mapped_column(String(1000), name="Content")
    from_user_id: Mapped[int] = mapped_column(ForeignKey("Users.ID"), name="FromUserID")
    to_user_id: Mapped[int] = mapped_column(ForeignKey("Users.ID"), name="ToUserID")

    def __init__(self, title, content, from_user_id, to_user_id):
        self.title = title
        self.content = content
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
