import { useAuth } from '../../../context/AuthContext'

export default function HomePage() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          टिकट साथी
        </h1>
        <p className="text-gray-500 text-lg mb-8">
          Book bus tickets anywhere in Nepal
        </p>
        {user && (
          <p className="text-blue-600 font-medium">
            Welcome back, {user.full_name || user.email} 👋
          </p>
        )}
      </div>
    </div>
  )
}
