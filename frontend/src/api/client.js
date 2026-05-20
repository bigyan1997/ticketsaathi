import axios from 'axios'

// All API calls go to the Django backend
const client = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// Before every request, attach the access token if we have one
// This means we never have to manually add "Authorization: Bearer ..." anywhere else
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// If a request fails with 401 (token expired), try refreshing the token once
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    // _retry flag prevents infinite loops if the refresh also fails
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      const refresh = localStorage.getItem('refresh')
      if (refresh) {
        try {
          const { data } = await axios.post('http://localhost:8000/api/auth/token/refresh/', {
            refresh,
          })
          localStorage.setItem('access', data.access)
          original.headers.Authorization = `Bearer ${data.access}`
          return client(original)
        } catch {
          // Refresh also failed — clear tokens so the user gets sent to login
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
        }
      }
    }

    return Promise.reject(error)
  }
)

export default client
