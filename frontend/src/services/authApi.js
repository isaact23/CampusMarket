import axios from 'axios';

export const get_homepage = async () => {
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

export const register = async (username, email, password) => {
    console.log("Sending registration request")

    try {
        const response = await axios.post('/api/register/', {
            username: username,
            email: email,
            password: password
        })
        console.log("Registered successfully")
        window.location = '/home'
        return response
    } catch (error) {
        if (error.status == 400) {
            console.log("Reigstration rejected")
        } else {
            console.error("Account creation failed:", error)
        }
        return null
    }
}

export const login = async (email, password, onFail) => {
    console.log("Sending login request")

    try {
        const response = await axios.post('/api/login/', {
            email: email,
            password: password
        })
        console.log("Logged in successfully")
        window.location = '/home'
        return response
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
};
