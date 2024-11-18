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

    constructor() {
        this.poolConnection = sql.connect(config)
        console.log('Connected to database')
    }
    
    close() {
        this.poolConnection.close()
        console.log('Disconnected from database')
    }
}
