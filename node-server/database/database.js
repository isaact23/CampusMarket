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
        console.log(res)
        console.log(res.rowsAffected[0])
        console.log(res.rowsAffected[0].ID)
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

        let res = await req.query(
            `SELECT * FROM dbo.Users WHERE Username = @username OR Email = @email`
        )
        
        // Handle username or email address already taken
        if (res.rowsAffected[0] > 0) {
            if (res.recordset[0].Username.Equals(user.username)) {
                throw new Error("A user with that username already exists")
            }
            else if (res.recordset[0].Email.Equals(user.email)) {
                throw new Error("A user with that email address already exists")
            }
            throw new Error("Error checking for existing user")
        }

        // Second request: Add user
        res = await req.query(
            `INSERT INTO dbo.Users (Username)
            OUTPUT INSERTED.ID
            VALUES (@username)`
        )

        if (res.rowsAffected[0] != 1) {
            throw new Error("Error adding user")
        }
        return res.recordset[0].ID
    }
    
    async connect() {
        console.log("Connecting to Azure SQL...")
        this.poolConnection = await sql.connect(config)
        console.log("Connected to Azure SQL.")
    }

    async close() {
        await this.poolConnection.close()
        console.log("Closed database connection")
    }
}
