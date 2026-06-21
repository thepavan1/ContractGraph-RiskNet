import axios from 'axios';

// Create an Axios instance with base URL pointing to the FastAPI backend
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
