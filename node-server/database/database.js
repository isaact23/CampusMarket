// From https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-nodejs

import sql from "mssql"

import {Transaction, Product, User, Message} from './types.js'

const config = {
    server: process.env["DB_SERVER"],
    port: +process.env["DB_PORT"],
    database: process.env["DB_DATABASE"],
    authentication: {
        type: 'azure-active-directory-default'
    },
    options: {
        encrypt: true
    }
}

export class Database {
    poolConnection = null

    checkConnection() {
        if (this.poolConnection == null)
            throw new Error("Cannot communicate with database.")
    }
    checkType(item, type) {
        if (!item instanceof type) {
            throw new Error("Incorrect type detected.")
        }
    }

    async getHomepage() {
        throw new Error("Not impl")
    }
    async searchProducts(query) {
        throw new Error("Not impl")
    }

    // Add a new product and return its ID.
    async addProduct(product) {
        this.checkConnection()
        this.checkType(product, Product)

        const req = this.poolConnection.request()

        req.input('name', sql.Text, product.name)
        req.input('description', sql.Text, product.description)
        req.input('price', sql.Decimal, product.price)
        req.input('owner_id', sql.Int, product.owner_id)

        const res = await req.query(
            `INSERT INTO dbo.Products (Name, Description, Price, OwnerID)
            OUTPUT INSERTED.ID
            VALUES (@name, @description, @price, @owner_id)`
        )

        if (res.rowsAffected[0] != 1) {
            throw new Error("Error adding product")
        }
        return res.recordset[0].ID
    }

    // Lookup a product by ID and return a Product object.
    // Return null if not found.
    async lookupProduct(id) {
        this.checkConnection()

        // Query database
        let req = this.poolConnection.request()
        req.input('id', sql.Int, id)
        let res = await req.query(
            `SELECT * FROM dbo.Products WHERE ID = @id`
        )

        // Handle item not found
        if (res.rowsAffected[0] != 1) {
            return null
        }

        // Create and populate Product object
        const rec = res.recordset[0]
        const product = new Product(rec.Name, rec.Description, rec.Price, rec.OwnerID)
        product.setID(rec.ID)
        return product
    }

    // Delete a product by ID.
    async deleteProduct(id) {
        throw new Error("Not impl")
    }

    // Add new user and return user ID. Throws error if
    // the user could not be created.
    async addUser(user) {
        this.checkConnection()
        this.checkType(user, User)

        // First request: Check for existing user
        let req = this.poolConnection.request()

        req.input('username', sql.VarChar(64), user.username)
        req.input('email', sql.VarChar(320), user.email)
        req.input('password', sql.VarChar(128), user.password)

        let res = await req.query(
            `SELECT * FROM dbo.Users WHERE Username = @username OR Email = @email`
        )
        
        // Handle username or email address already taken
        if (res.rowsAffected[0] > 0) {
            if (res.recordset[0].Username == user.username) {
                throw new Error("A user with that username already exists")
            }
            else if (res.recordset[0].Email == user.email) {
                throw new Error("A user with that email address already exists")
            }
            throw new Error("Error checking for existing user")
        }

        // Second request: Add user
        res = await req.query(
            `INSERT INTO dbo.Users (Username, Email, Password)
            OUTPUT INSERTED.ID
            VALUES (@username, @email, @password)`
        )

        if (res.rowsAffected[0] != 1) {
            throw new Error("Error adding user")
        }
        return res.recordset[0].ID
    }

    // Lookup a user by ID and return the User data.
    // Return null if not found.
    async lookupUser(id) {
        this.checkConnection()

        // Query database
        let req = this.poolConnection.request()
        req.input('id', sql.Int, id)
        let res = await req.query(
            `SELECT * FROM dbo.Users WHERE ID = @id`
        )

        // Handle item not found
        if (res.rowsAffected[0] != 1) {
            return null
        }

        // Create and populate User object
        const rec = res.recordset[0]
        const user = new User(rec.Username, rec.Email, null)
        user.setID(rec.ID)
        return user
    }

    // Delete a user by ID.
    async deleteUser(id) {
        throw new Error("Not impl")
    }

    // Create a new message and return the message ID.
    async addMessage(message) {
        this.checkConnection()
        this.checkType(message, Message)

        const req = this.poolConnection.request()

        req.input('to_id', sql.Int, message.to_id)
        req.input('from_id', sql.Int, message.from_id)
        req.input('title', sql.Text, message.title)
        req.input('content', sql.Text, message.content)

        const res = await req.query(
            `INSERT INTO dbo.Messages (ToUserID, FromUserID, Title, Content)
            OUTPUT INSERTED.ID
            VALUES (@to_id, @from_id, @title, @content)`
        )

        if (res.rowsAffected[0] != 1) {
            throw new Error("Error adding message")
        }
        return res.recordset[0].ID
    }

    // Lookup a message by ID and return a Message object.
    // Return null if not found.
    async lookupMessage(id) {
        this.checkConnection()

        // Query database
        let req = this.poolConnection.request()
        req.input('id', sql.Int, id)
        let res = await req.query(
            `SELECT * FROM dbo.Messages WHERE ID = @id`
        )

        // Handle item not found
        if (res.rowsAffected[0] != 1) {
            return null
        }

        // Create and populate Message object
        const rec = res.recordset[0]
        const message = new Message(rec.ToID, rec.FromID, rec.Title, rec.Content)
        message.setID(rec.ID)
        return message
    }

    // Delete a message by ID.
    async deleteMessage(id) {
        throw new Error("Not impl")
    }

    // Create a new transaction and return its ID.
    async addTransaction(transaction) {
        this.checkConnection()
        this.checkType(transaction, Transaction)

        const req = this.poolConnection.request()

        req.input('product_id', sql.Int, transaction.product_id)
        req.input('buyer_id', sql.Int, transaction.buyer_id)
        req.input('seller_id', sql.Int, transaction.seller_id)

        const res = await req.query(
            `INSERT INTO dbo.Transactions (ProductID, BuyingUserID, SellingUserID)
            OUTPUT INSERTED.ID
            VALUES (@product_id, @buyer_id, @seller_id)`
        )

        if (res.rowsAffected[0] != 1) {
            throw new Error("Error adding transaction")
        }
        return res.recordset[0].ID
    }
    
    // Lookup a transaction by ID and return a Transaction object.
    // Return null if not found.
    async lookupTransaction(id) {
        this.checkConnection()

        // Query database
        let req = this.poolConnection.request()
        req.input('id', sql.Int, id)
        let res = await req.query(
            `SELECT * FROM dbo.Transactions WHERE ID = @id`
        )

        // Handle item not found
        if (res.rowsAffected[0] != 1) {
            return null
        }

        // Create and populate Transaction object
        const rec = res.recordset[0]
        const transaction = new Transaction(rec.ProductID, rec.BuyingUserID, rec.SellingUserID)
        transaction.setID(rec.ID)
        return transaction
    }

    async connect() {
        console.log("Connecting to Azure SQL...")
        while (this.poolConnection == null) {
            try {
                this.poolConnection = await sql.connect(config)
            }
            catch {
                console.log("Trying again to connect to Azure SQL...")
            }
        }
        console.log("Connected to Azure SQL.")
    }

    async close() {
        await this.poolConnection.close()
        console.log("Closed database connection")
    }
}
