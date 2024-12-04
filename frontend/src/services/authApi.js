import axios from 'axios'
import { useState } from 'react'

class AuthApi {
    constructor() {
        [this.email, this.setEmail] = useState('')
        [this.token, this.setToken] = useState('')
    }

    getEmail = () => this.email
    getToken = () => this.token

    setEmail = (email) => this.setEmail(email)
    setToken = (token) => this.setToken(token)

    get_homepage = async () => {
        console.log("Getting homepage products")
    
        try {
            const response = await axios.post("/api/homepage/", {})
            console.log("Got homepage data")
            return response
        } catch (error) {
            console.error("Retrieving homepage data failed:", error)
            return null
        }
    }

    register = async (username, email, password, onSuccess, onFail) => {
        console.log("Sending registration request")
    
        try {
            const response = await axios.post('/api/register/', {
                username: username,
                email: email,
                password: password
            })
            console.log("Registered successfully")
            onSuccess(response.data.token)
        } catch (error) {
            if (error.status == 400) {
                console.log("Reigstration rejected")
                onFail("Could not register. Try different credentials.")
            } else {
                console.error("Account creation failed:", error)
                onFail("Registration failed. Please try again later.")
            }
            return null
        }
    }

    login = async (email, password, onSuccess, onFail) => {
        console.log("Sending login request")
    
        try {
            const response = await axios.post('/api/login/', {
                email: email,
                password: password
            })
            console.log("Logged in successfully")
            onSuccess(response.data.token)
        } catch (error) {
            if (error.status == 400) {
                console.log("Login rejected")
                onFail("Incorrect email or password.")
            } else {
                console.error("Login failed:", error)
                onFail("Login failed. Please try again later.")
            }
            return null
        }
    }

    logout = () => {
        this.username = ''
        this.email = ''
        this.password = ''
    }
}
