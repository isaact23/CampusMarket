class Message:
    def __init__(this, to_id, from_id, title, content):
        this.to_id = to_id
        this.from_id = from_id
        this.title = title
        this.content = content

class Transaction:
    def __init__(this, product_id, buying_user_id, selling_user_id):
        this.product_id = product_id
        this.buying_user_id = buying_user_id
        this.selling_user_id = selling_user_id

class Product:
    def __init__(this, name, description, price, owner_id):
        this.name = name
        this.description = description
        this.price = price
        this.owner_id = owner_id

class User:
    def __init__(this, username):
        this.username = username

class Query:
    def __init__(this, text):
        this.text = text