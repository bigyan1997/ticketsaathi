import client from './client'

// Create a new account
export const register = (data) =>
  client.post('/auth/register/', data)

// Log in — returns { access, refresh } tokens
export const login = (data) =>
  client.post('/auth/login/', data)

// Get the currently logged-in user's profile
export const getProfile = () =>
  client.get('/auth/profile/')

// Update the logged-in user's profile
export const updateProfile = (data) =>
  client.put('/auth/profile/', data)
