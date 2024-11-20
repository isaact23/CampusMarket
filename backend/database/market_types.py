class Message:
    def __init__(this, to_id, from_id, title, content):
        this.id = None
        this.to_id = to_id
        this.from_id = from_id
        this.title = title
        this.content = content
    def set_id(this, id):
        this.id = id

class Transaction:
    def __init__(this, product_id, buyer_id, seller_id):
        this.id = None
        this.product_id = product_id
        this.buyer_id = buyer_id
        this.seller_id = seller_id
    def set_id(this, id):
        this.id = id

class Product:
    def __init__(this, name, description, price, owner_id):
        this.id = None
        this.name = name
        this.description = description
        this.price = price
        this.owner_id = owner_id
    def set_id(this, id):
        this.id = id

class User:
    def __init__(this, username, email, password):
        this.id = None
        this.username = username
        this.email = email
        this.password = password
    def set_id(this, id):
        this.id = id

class Query:
    def __init__(this, text):
        this.text = text