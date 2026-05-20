import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import PrivateRoute from './components/PrivateRoute'

// Auth
import LoginPage from './features/auth/pages/LoginPage'
import RegisterPage from './features/auth/pages/RegisterPage'

// Trips (home)
import HomePage from './features/trips/pages/HomePage'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        {/* Public routes */}
        <Route path="/login"    element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes — redirect to /login if not logged in */}
        <Route path="/" element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        } />

        {/* Catch-all — redirect unknown URLs to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
