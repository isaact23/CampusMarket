import axios from 'axios';

export const register = async (username, email, password) => {
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
    try {
        const response = await axios.post('/login/oauth/token', {
            grant_type: 'password',
            username: username,
            password: password,
            client_id: '7yFnbiDquoRvw8Xwdxncdo2YBpSEHpqq',
            client_secret: 'VVHVDJfKWsX2u9rcJwDEyL5wvSJxJ3yTmX3aDkm01fFZowNbsiIaot5SPxwAg1Y9'
        });
        console.log("Logged in successfully")
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error("Log in failed:", error);
        return null;
    }
};
