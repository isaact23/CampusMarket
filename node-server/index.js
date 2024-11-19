import express from "express"
import path from "path"
import apiRoutes from './routes/api.js'
import {Database} from './database/database.js'
import {Transaction, Product, User, Message} from './database/types.js'

const BUILD = path.join(import.meta.dirname, "../react-app/dist/")
const PORT = 3000

const app = express()
const database = new Database()

app.use("/", express.static(BUILD))
app.use(express.json())
app.use("/api", apiRoutes)

app.get("*", (req, res) => {
    res.sendFile(path.join(BUILD, "index.html"))
})

const server = await startup()
process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)

async function startup() {
    await database.connect()

    database.addProduct(new Product('Ice', 'Coolant stuff', 4.0, 1))
    //const newId = await database.addUser(new User("shuffles1", "shuffles2@gmail.com"))
    //console.log("ID: ", newId)

    return app.listen(PORT, () => {
        console.log(`CampusMarket server listening on ${PORT}`)
    })
}

async function shutdown() {
    await database.close()
    await server.close()
}
