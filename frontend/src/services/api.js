// src/services/api.js
export class ApiError extends Error {
    constructor(message, status) {
      super(message);
      this.status = status;
    }
  }
  
  export const api = {
    async get(endpoint) {
      try {
        const response = await fetch(`/api/${endpoint}`);
        if (!response.ok) {
          throw new ApiError(`API Error: ${response.statusText}`, response.status);
        }
        return response.json();
      } catch (error) {
        throw error;
      }
    },
  
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
          throw new ApiError(`API Error: ${response.statusText}`, response.status);
        }
        return response.json();
      } catch (error) {
        throw error;
      }
    }
    // Add other methods (PUT, DELETE, etc.) as needed
  }