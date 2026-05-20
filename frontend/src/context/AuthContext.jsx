import { createContext, useContext, useState, useEffect } from 'react'
import { getProfile } from '../api/auth'

// This context makes the logged-in user available to every component in the app
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true) // true while we check if user is already logged in

  // On first load, check if tokens exist in localStorage and fetch the user's profile
  useEffect(() => {
    const access = localStorage.getItem('access')
    if (access) {
      getProfile()
        .then((res) => setUser(res.data))
        .catch(() => {
          // Token invalid or expired — clear everything
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  // Called after a successful login — saves tokens and sets the user
  const login = (tokens, userData) => {
    localStorage.setItem('access', tokens.access)
    localStorage.setItem('refresh', tokens.refresh)
    setUser(userData)
  }

  // Called when the user clicks logout — wipes everything
  const logout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook — instead of writing useContext(AuthContext) everywhere, just write useAuth()
export const useAuth = () => useContext(AuthContext)
