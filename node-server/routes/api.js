import express from "express"
const router = express.Router()

router.post("/login", (req, res) => {
    console.log("Got login request")
    console.log(req.email, req.password)
})

router.post("/register", (req, res) => {
    console.log("Got register request")
    console.log(req.email, req.username, req.password)

    
})

export default router