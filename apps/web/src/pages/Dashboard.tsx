import { useAuthStore } from '../store/auth'
import { useNavigate } from 'react-router-dom'

export default function DashboardPage() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-glass-bg">
      <nav className="glass border-b border-glass-border">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gradient">نظام الخدمة</h1>
          <div className="flex items-center gap-4">
            <span className="text-glass-text">{user?.displayName || user?.email}</span>
            <button
              onClick={handleLogout}
              className="glass-button-secondary"
            >
              تسجيل الخروج
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto p-6">
        <div className="glass-card mb-8">
          <h2 className="text-2xl font-bold text-glass-text mb-4">
            مرحباً بك في نظام الخدمة
          </h2>
          <p className="text-glass-muted mb-4">
            نسخة جديدة محسّنة من نظام إدارة الحضور والغياب
          </p>
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="glass p-4 rounded-lg text-center">
              <p className="text-sm text-glass-muted">الحالة</p>
              <p className="text-lg font-bold text-glass-text mt-2">
                {user?.role === 'admin' && 'مسؤول'}
                {user?.role === 'servant' && 'خادم'}
                {user?.role === 'viewer' && 'مشاهد'}
                {user?.role === 'user' && 'مستخدم'}
              </p>
            </div>
            <div className="glass p-4 rounded-lg text-center">
              <p className="text-sm text-glass-muted">البريد الإلكتروني</p>
              <p className="text-lg font-bold text-glass-text mt-2 truncate">
                {user?.email}
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              التسجيل اليومي
            </h3>
            <p className="text-glass-muted text-sm">جاري التطوير...</p>
          </div>
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              لوحة البيانات
            </h3>
            <p className="text-glass-muted text-sm">جاري التطوير...</p>
          </div>
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              تقرير الغياب
            </h3>
            <p className="text-glass-muted text-sm">جاري التطوير...</p>
          </div>
        </div>
      </main>
    </div>
  )
}
