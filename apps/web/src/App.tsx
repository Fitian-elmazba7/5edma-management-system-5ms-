import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from './store/auth'
import LoginPage from './pages/Login'
import DashboardPage from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'

export default function App() {
  const { user, loading } = useAuthStore()

  useEffect(() => {
    // Initialize auth state
    useAuthStore.getState().initializeAuth()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-glass-bg flex items-center justify-center">
        <div className="glass-card">
          <p className="text-glass-text">جاري التحميل...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            user ? <DashboardPage /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        {/* Additional routes will be added in Phase 4 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}
