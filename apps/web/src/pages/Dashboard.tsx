import { useAuthStore } from '../store/auth'
import { useNavigate, useLocation } from 'react-router-dom'
import { GlassButton, GlassCard } from '../components/ui'

export default function DashboardPage() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  // Navigation items based on role
  const getNavItems = () => {
    const baseItems = [
      { label: 'لوحة البيانات', path: '/dashboard', roles: ['admin', 'servant', 'viewer', 'user'] },
      { label: '📊 الإحصائيات', path: '/stats', roles: ['admin', 'servant', 'viewer', 'user'] },
    ]

    const roleBasedItems = {
      admin: [
        { label: '📝 التسجيل', path: '/registration', roles: ['admin'] },
        { label: '📋 الغياب', path: '/absence', roles: ['admin'] },
        { label: '📊 إدارة البيانات', path: '/data', roles: ['admin'] },
        { label: '⏰ الحضور المبكر', path: '/early-arrival', roles: ['admin'] },
        { label: '📋 تقرير الحضور', path: '/attendance-report', roles: ['admin'] },
        { label: '📈 المقارنة', path: '/comparison', roles: ['admin'] },
        { label: '👥 المستخدمين', path: '/users', roles: ['admin'] },
      ],
      servant: [
        { label: '📝 التسجيل', path: '/registration', roles: ['servant'] },
        { label: '📋 الغياب', path: '/absence', roles: ['servant'] },
        { label: '⏰ الحضور المبكر', path: '/early-arrival', roles: ['servant'] },
        { label: '📋 تقرير الحضور', path: '/attendance-report', roles: ['servant'] },
        { label: '📈 المقارنة', path: '/comparison', roles: ['servant'] },
      ],
      viewer: [
        { label: '📈 المقارنة', path: '/comparison', roles: ['viewer', 'user'] },
      ],
      user: [
        { label: '📈 المقارنة', path: '/comparison', roles: ['user'] },
      ],
    }

    const userRoleItems = roleBasedItems[user?.role || 'viewer'] || []
    return [...baseItems, ...userRoleItems]
  }

  const navItems = getNavItems()

  return (
    <div className="min-h-screen bg-glass-bg">
      {/* Header */}
      <header className="glass border-b border-glass-border sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold text-gradient">نظام الخدمة</h1>
              <span className="text-xs px-3 py-1 rounded-full bg-blue-500/20 text-blue-300">
                v2.0
              </span>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-right">
                <p className="text-sm text-glass-text font-medium">
                  {user?.displayName || user?.email}
                </p>
                <p className="text-xs text-glass-muted">
                  {user?.role === 'admin' && 'مسؤول النظام'}
                  {user?.role === 'servant' && 'خادم'}
                  {user?.role === 'viewer' && 'مشاهد'}
                  {user?.role === 'user' && 'مستخدم'}
                </p>
              </div>
              <GlassButton
                variant="secondary"
                size="sm"
                onClick={handleLogout}
              >
                تسجيل الخروج
              </GlassButton>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex gap-1 mt-4 -mx-6 px-6 border-t border-glass-border/50 pt-4">
            {navItems.map((item) => (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`px-4 py-2 rounded-lg transition-colors font-medium text-sm ${
                  location.pathname === item.path
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                    : 'text-glass-muted hover:text-glass-text hover:bg-blue-500/10'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6">
        <GlassCard className="mb-8">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-3xl font-bold text-glass-text mb-2">
                مرحباً بك في نظام الخدمة
              </h2>
              <p className="text-glass-muted">
                نسخة جديدة محسّنة من نظام إدارة الحضور والغياب للكنيسة القبطية الأرثوذكسية
              </p>
            </div>
            <div className="text-4xl">⛪</div>
          </div>

          <div className="grid grid-cols-3 gap-4 mt-8">
            <div className="glass p-4 rounded-lg text-center">
              <p className="text-sm text-glass-muted mb-2">الدور الوظيفي</p>
              <p className="text-2xl font-bold text-glass-primary">
                {user?.role === 'admin' && '👑 مسؤول'}
                {user?.role === 'servant' && '🙏 خادم'}
                {user?.role === 'viewer' && '👁️ مشاهد'}
                {user?.role === 'user' && '👤 مستخدم'}
              </p>
            </div>
            <div className="glass p-4 rounded-lg text-center">
              <p className="text-sm text-glass-muted mb-2">البريد الإلكتروني</p>
              <p className="text-lg font-bold text-glass-text truncate">
                {user?.email}
              </p>
            </div>
            <div className="glass p-4 rounded-lg text-center">
              <p className="text-sm text-glass-muted mb-2">الحالة</p>
              <p className="text-lg font-bold text-green-300">
                ✓ متصل
              </p>
            </div>
          </div>
        </GlassCard>

        {/* Feature cards - placeholder */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <GlassCard>
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              📝 التسجيل اليومي
            </h3>
            <p className="text-glass-muted text-sm mb-4">
              تسجيل حضور الأطفال بسهولة
            </p>
            <GlassButton
              variant="secondary"
              size="sm"
              fullWidth
              disabled
            >
              قيد التطوير
            </GlassButton>
          </GlassCard>

          <GlassCard>
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              📊 لوحة البيانات
            </h3>
            <p className="text-glass-muted text-sm mb-4">
              إحصائيات وتقارير الحضور
            </p>
            <GlassButton
              variant="secondary"
              size="sm"
              fullWidth
              disabled
            >
              قيد التطوير
            </GlassButton>
          </GlassCard>

          <GlassCard>
            <h3 className="text-lg font-semibold text-glass-text mb-2">
              ⚙️ الإعدادات
            </h3>
            <p className="text-glass-muted text-sm mb-4">
              إدارة إعدادات النظام
            </p>
            <GlassButton
              variant="secondary"
              size="sm"
              fullWidth
              disabled
            >
              قيد التطوير
            </GlassButton>
          </GlassCard>
        </div>
      </main>
    </div>
  )
}
