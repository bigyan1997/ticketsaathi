import { Link } from 'react-router-dom'
import RegisterForm from '../components/RegisterForm'
import GoogleButton from '../components/GoogleButton'

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-gray-200 p-8">

        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
          <p className="text-sm text-gray-500 mt-1">Book bus tickets anywhere in Nepal</p>
        </div>

        {/* Google OAuth */}
        <GoogleButton />

        {/* Divider */}
        <div className="flex items-center gap-3 my-5">
          <div className="flex-1 h-px bg-gray-200" />
          <span className="text-xs text-gray-400">or register with email</span>
          <div className="flex-1 h-px bg-gray-200" />
        </div>

        {/* Registration form */}
        <RegisterForm />

        {/* Link to login */}
        <p className="text-sm text-center text-gray-500 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-blue-600 hover:underline font-medium">
            Sign in
          </Link>
        </p>

      </div>
    </div>
  )
}
