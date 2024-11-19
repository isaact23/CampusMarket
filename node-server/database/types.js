export class Message {
    constructor(to_id, from_id, title, content) {
        this.id = null
        this.to_id = to_id
        this.from_id = from_id
        this.title = title
        this.content = content
    }
    set_id(id) {
        this.id = id
    }
}

export class Transaction {
    constructor(product_id, buying_user_id, selling_user_id) {
        this.id = null
        this.product_id = product_id
        this.buyer_id = buying_user_id
        this.seller_id = selling_user_id
    }
    set_id(id) {
        this.id = id
    }
}

export class Product {
    constructor(name, description, price, owner_id) {
        this.id = null
        this.name = name
        this.description = description
        this.price = price
        this.owner_id = owner_id
    }
    set_id(id) {
        this.id = id
    }
}

export class User {
    constructor(username, email, password) {
        this.id = null
        this.username = username
        this.email = email
        this.password = password
    }
    set_id(id) {
        this.id = id
    }
}

export class Query {
    constructor(text) {
        this.text = text
    }
}
