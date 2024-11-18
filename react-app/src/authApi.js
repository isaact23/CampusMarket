import axios from 'axios';

export const register = async (username, email, password) => {
    console.log("Handling registration")
    console.log('Username:', username, 'Email:', email, 'Password:', password);

    // TODO: Implement registration via django

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

export const login = async (username, password) => {
    console.log("Handling login")
    console.log('Email:', email, 'Password:', password);

    // TODO: Implement logging in via django

    /*try {
        const response = await axios.post('/loginAPI/authorize', {
            response_type: 'token',
            username: username,
            password: password,
            client_id: CLIENT_ID
        });
        console.log("Logged in successfully")
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error("Log in failed:", error);
        return null;
    }*/
};
