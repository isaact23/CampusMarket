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

console.log(config)

connect();

async function connect() {
    try {
        var poolConnection = await sql.connect(config)
        console.log('yay')
        poolConnection.close()
    }
    catch (err) {
        console.error(err.message)
    }
}