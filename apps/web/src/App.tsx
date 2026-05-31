import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from './store/auth'
import LoginPage from './pages/Login'
import DashboardPage from './pages/Dashboard'
import RegistrationPage from './pages/Registration'
import DashboardStatsPage from './pages/DashboardStats'
import AbsencePage from './pages/Absence'
import DataManagementPage from './pages/DataManagement'
import EarlyArrivalPage from './pages/EarlyArrival'
import AttendanceReportPage from './pages/AttendanceReport'
import ComparisonReportPage from './pages/ComparisonReport'
import UsersPage from './pages/Users'
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
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        {/* Feature Pages */}
        <Route
          path="/registration"
          element={
            <ProtectedRoute requiredRole={['admin', 'servant']}>
              <RegistrationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/stats"
          element={
            <ProtectedRoute>
              <DashboardStatsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/absence"
          element={
            <ProtectedRoute requiredRole={['admin', 'servant']}>
              <AbsencePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/data"
          element={
            <ProtectedRoute requiredRole="admin">
              <DataManagementPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/early-arrival"
          element={
            <ProtectedRoute requiredRole={['admin', 'servant']}>
              <EarlyArrivalPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/attendance-report"
          element={
            <ProtectedRoute requiredRole={['admin', 'servant']}>
              <AttendanceReportPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/comparison"
          element={
            <ProtectedRoute>
              <ComparisonReportPage />
            </ProtectedRoute>
          }
        />

        {/* Admin Routes */}
        <Route
          path="/users"
          element={
            <ProtectedRoute requiredRole="admin">
              <UsersPage />
            </ProtectedRoute>
          }
        />

        {/* Redirect root to dashboard if authenticated */}
        <Route
          path="/"
          element={
            user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
          }
        />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}
