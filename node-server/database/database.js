// From https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-nodejs

import sql from "mssql"

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

    constructor() {
        console.log("Connecting to Azure SQL...")
        sql.connect(config)
        .then(pool => {
            this.poolConnection = pool
            console.log("Connected to Azure SQL.")
        })
        .catch(() => {
            console.error("Failed to connect to Azure SQL")
        })
    }
    
    async close() {
        await this.poolConnection.close()
        console.log("Closed database connection")
    }
}
