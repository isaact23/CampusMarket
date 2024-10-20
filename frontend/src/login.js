import axios from 'axios';

export const login = async (username, password) => {
    try {
        const response = await axios.post('https://dev-wwzvhvto6t4diopr.us.auth0.com/oauth/token', {
            grant_type: 'password',
            username: username,
            password: password,
            client_id: '7yFnbiDquoRvw8Xwdxncdo2YBpSEHpqq',
            audience: 'https://dev-wwzvhvto6t4diopr.us.auth0.com/api/v2/',
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
};
