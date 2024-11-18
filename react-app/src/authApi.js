import axios from 'axios';

export const register = async (username, email, password) => {
    console.log("Handling registration")
    console.log('Username:', username, 'Email:', email, 'Password:', password);

    try {
        const response = await axios.post('/api/register', {
            username: username,
            email: email,
            password: password
        })
        console.log("Account created successfully")
        console.log(response)
        return response
    } catch (error) {
        console.error("Account creation failed:", error)
        return null
    }
}

export const login = async (email, password) => {
    console.log("Handling login")
    console.log('Email:', email, 'Password:', password);

    try {
        const response = await axios.post('/api/login', {
            email: email,
            password: password
        })
        console.log("Logged in successfully")
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error("Log in failed:", error);
        return null;
    }
};
