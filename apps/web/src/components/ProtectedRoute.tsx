import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'
import { UserRole } from '@5edma/shared'

interface ProtectedRouteProps {
  children: ReactNode
  requiredRole?: UserRole | UserRole[]
}

export default function ProtectedRoute({
  children,
  requiredRole,
}: ProtectedRouteProps) {
  const { user, loading } = useAuthStore()

  if (loading) {
    return (
      <div className="min-h-screen bg-glass-bg flex items-center justify-center">
        <div className="glass-card">
          <p className="text-glass-text">جاري التحميل...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole) {
    const roles = Array.isArray(requiredRole) ? requiredRole : [requiredRole]
    if (!roles.includes(user.role)) {
      return (
        <div className="min-h-screen bg-glass-bg flex items-center justify-center">
          <div className="glass-card max-w-md">
            <p className="text-glass-text text-center">
              ليس لديك صلاحيات للوصول لهذه الصفحة
            </p>
          </div>
        </div>
      )
    }
  }

  return <>{children}</>
}
