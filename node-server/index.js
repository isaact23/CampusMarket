import express from "express"
import path from "path"
import apiRoutes from './routes/api.js'
import {Database} from './database/database.js'

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

const server = app.listen(PORT, () => {
    console.log(`CampusMarket server listening on ${PORT}`)
})

function shutdown() {
    database.close()

    server.close(err => {
        if (err) {
            console.error("Error shutting down express server:" + err)
            exit(1)
        } else {
            console.log("Server shut down successfully")
            exit(0)
        }
    })
}

process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)
