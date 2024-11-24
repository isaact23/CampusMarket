import axios from 'axios';

export const register = async (username, email, password) => {
    console.log("Sending registration request")

    try {
        const response = await axios.post('/api/register/', {
            username: username,
            email: email,
            password: password
        })
        console.log("Registered successfully")
        return response
    } catch (error) {
        console.error("Account creation failed:", error)
        return null
    }
}

export const login = async (email, password) => {
    console.log("Sending login request")

    try {
        const response = await axios.post('/api/login/', {
            email: email,
            password: password
        })
        console.log("Logged in successfully")
        return response
    } catch (error) {
        console.error("Login failed:", error)
        return null
    }
};
