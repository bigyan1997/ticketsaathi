import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// Wrap any page with this to require login
// If the user is not logged in, they get redirected to /login
export default function PrivateRoute({ children }) {
  const { user, loading } = useAuth()

  // Wait until we know if the user is logged in before deciding
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return children
}
