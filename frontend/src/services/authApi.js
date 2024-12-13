import axios from 'axios'

export default class AuthApi {
    constructor() {
        this.email = ''
        this.token = ''
        this.isLoggedIn = true
    }

    getEmail = () => this.email
    getToken = () => this.token

    setEmail = (email) => {this.email = email; console.log("Set email to " + email)}
    setToken = (token) => this.token = token

    getIsLoggedIn = () => this.isLoggedIn

    getHomepage = async () => {
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
            this.isLoggedIn = true
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
        this.email = ''
        this.token = ''
        this.isLoggedIn = false
    }

    /* Send a GET request to the backend without authentication. */
    async get(endpoint) {
        try {
          const response = await fetch(`/api/${endpoint}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`, response.status);
          }
          return response.json();
        } catch (error) {
          throw error;
        }
    }

    /* Send a GET request to the backend with authentication. */
    async getAuth(endpoint) {
        if (this.token.length == 0) {
            throw new Error("Cannot run getAuth without authorization")
        }
        try {
          const response = await fetch(`/api/${endpoint}`, {
            method: 'GET',
            headers: {
                'Authorization': this.email + ',' + this.token,
                'Content-Type': 'application/json',
            }
          });
          if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`, response.status);
          }
          return response.json();
        } catch (error) {
          throw error;
        }
    }

    /* Send a POST request to the backend without authentication. */
    async post(endpoint, data) {
        try {
          const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });
          if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`, response.status);
          }
          return response.json();
        } catch (error) {
          throw error;
        }
    }

    /* Send a POST request to the backend with authentication. */
    async postAuth(endpoint, data) {
        if (this.token.length == 0) {
            throw new Error("Cannot run postAuth without authorization")
        }
        try {
          const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': this.email + ',' + this.token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });
          if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`, response.status);
          }
          return response.json();
        } catch (error) {
          throw error;
        }
    }
}
