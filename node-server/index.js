import express from "express"
import path from "path"

import apiRoutes from './routes/api.js'

const BUILD = path.join(import.meta.dirname, "../react-app/dist/")
const PORT = 3000

const app = express()

app.use("/", express.static(BUILD))
app.use(express.json())
app.use("/api", apiRoutes)

app.get("*", (req, res) => {
    res.sendFile(path.join(BUILD, "index.html"))
})

app.listen(PORT, () => {
    console.log(`CampusMarket server listening on ${PORT}`)
})
