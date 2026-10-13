import axios, { AxiosError } from 'axios'

// API base URL defaults to '/api' (proxied via Vite dev server to localhost:8080)
// Can be customized via VITE_API_BASE_URL in environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Hooks for auth tokens (e.g., Bearer JWT) can be added here
    return config
  },
  (error) => Promise.reject(error),
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ message?: string }>) => {
    const message =
      error.response?.data?.message ||
      error.message ||
      'An unexpected REST API error occurred'

    return Promise.reject(new Error(message))
  },
)

export default apiClient
