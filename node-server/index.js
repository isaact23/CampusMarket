import express from "express"
import path from "path"

const BUILD = path.join(import.meta.dirname, "../react-app/dist/")
const PORT = 3000

const app = express()
app.use("/", express.static(BUILD))
app.listen(PORT, () => {
    console.log(`CampusMarket server listening on ${PORT}`)
})
