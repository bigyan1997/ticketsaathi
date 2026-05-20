import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">

        <Link to="/" className="font-bold text-blue-600 text-lg">
          टिकट साथी
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm text-gray-600">{user.full_name || user.email}</span>
              <Link to="/profile" className="text-sm text-gray-600 hover:text-blue-600">
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="text-sm text-red-500 hover:text-red-600 cursor-pointer"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm text-gray-600 hover:text-blue-600">
                Login
              </Link>
              <Link
                to="/register"
                className="text-sm bg-blue-600 text-white px-4 py-1.5 rounded-lg hover:bg-blue-700"
              >
                Register
              </Link>
            </>
          )}
        </div>

      </div>
    </nav>
  )
}
