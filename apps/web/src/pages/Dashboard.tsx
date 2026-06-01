import { useEffect } from 'react';
import { useAuthStore } from '../store/auth';
import { useNavigate, useLocation } from 'react-router-dom';
import { GlassCard, CopticButton, DataTable } from '../components/coptic';
import { useNavigation } from '../context/NavigationContext';

export default function DashboardPage() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const { setCurrentSection } = useNavigation();

  useEffect(() => {
    setCurrentSection('dashboard');
  }, [setCurrentSection]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // Navigation items based on role
  const getNavItems = () => {
    const baseItems = [
      { label: 'لوحة البيانات', path: '/dashboard', roles: ['admin', 'servant', 'viewer', 'user'] },
      { label: '📊 الإحصائيات', path: '/stats', roles: ['admin', 'servant', 'viewer', 'user'] },
    ];

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
    };

    const userRoleItems = roleBasedItems[user?.role as keyof typeof roleBasedItems || 'viewer'] || [];
    return [...baseItems, ...userRoleItems];
  };

  const navItems = getNavItems();

  return (
    <div className="min-h-screen bg-navy-deep text-cream">
      {/* Header */}
      <header className="backdrop-blur-glass border-b border-gold-primary/20 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <h1 className="text-3xl font-display font-bold text-gold-primary">نظام الخدمة</h1>
              <span className="text-xs px-3 py-1 rounded-full bg-gold-primary/20 text-gold-accent">
                v2.0
              </span>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-right">
                <p className="text-sm font-body font-medium text-cream">
                  {user?.displayName || user?.email}
                </p>
                <p className="text-xs text-text-muted font-body">
                  {user?.role === 'admin' && 'مسؤول النظام'}
                  {user?.role === 'servant' && 'خادم'}
                  {user?.role === 'viewer' && 'مشاهد'}
                  {user?.role === 'user' && 'مستخدم'}
                </p>
              </div>
              <CopticButton
                variant="secondary"
                onClick={handleLogout}
              >
                تسجيل الخروج
              </CopticButton>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex gap-1 mt-4 -mx-6 px-6 border-t border-gold-primary/20 pt-4 overflow-x-auto">
            {navItems.map((item) => (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`px-4 py-2 rounded-lg transition-all font-medium text-sm whitespace-nowrap ${
                  location.pathname === item.path
                    ? 'bg-gold-primary/20 text-gold-primary border border-gold-primary/50 shadow-gold-glow'
                    : 'text-text-muted hover:text-cream hover:bg-gold-primary/10'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Welcome Section */}
        <GlassCard variant="default">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-4xl font-display font-bold text-cream mb-2">
                مرحباً بك في نظام الخدمة
              </h2>
              <p className="font-body text-text-muted text-lg">
                نسخة جديدة محسّنة من نظام إدارة الحضور والغياب للكنيسة القبطية الأرثوذكسية
              </p>
            </div>
            <div className="text-5xl">⛪</div>
          </div>

          {/* User Info Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <GlassCard variant="stat">
              <div className="text-gold-accent text-xs font-bold uppercase tracking-wider mb-2">
                الدور الوظيفي
              </div>
              <div className="text-cream text-2xl font-display font-bold">
                {user?.role === 'admin' && '👑 مسؤول'}
                {user?.role === 'servant' && '🙏 خادم'}
                {user?.role === 'viewer' && '👁️ مشاهد'}
                {user?.role === 'user' && '👤 مستخدم'}
              </div>
            </GlassCard>

            <GlassCard variant="stat">
              <div className="text-gold-accent text-xs font-bold uppercase tracking-wider mb-2">
                البريد الإلكتروني
              </div>
              <div className="text-cream text-sm font-body truncate">
                {user?.email}
              </div>
            </GlassCard>

            <GlassCard variant="stat">
              <div className="text-gold-accent text-xs font-bold uppercase tracking-wider mb-2">
                الحالة
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                <span className="text-cream font-body">متصل</span>
              </div>
            </GlassCard>
          </div>
        </GlassCard>

        {/* Feature cards - Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Daily Registration */}
          <GlassCard variant="default">
            <h3 className="text-lg font-display font-semibold text-cream mb-2">
              📝 التسجيل اليومي
            </h3>
            <p className="font-body text-text-muted text-sm mb-6">
              تسجيل حضور الأطفال بسهولة وسرعة
            </p>
            <CopticButton
              variant="secondary"
              disabled
              className="w-full"
            >
              قيد التطوير
            </CopticButton>
          </GlassCard>

          {/* Statistics Dashboard */}
          <GlassCard variant="default">
            <h3 className="text-lg font-display font-semibold text-cream mb-2">
              📊 لوحة البيانات
            </h3>
            <p className="font-body text-text-muted text-sm mb-6">
              إحصائيات وتقارير الحضور الشاملة
            </p>
            <CopticButton
              variant="secondary"
              disabled
              className="w-full"
            >
              قيد التطوير
            </CopticButton>
          </GlassCard>

          {/* System Settings */}
          <GlassCard variant="default">
            <h3 className="text-lg font-display font-semibold text-cream mb-2">
              ⚙️ الإعدادات
            </h3>
            <p className="font-body text-text-muted text-sm mb-6">
              إدارة إعدادات النظام والمستخدمين
            </p>
            <CopticButton
              variant="secondary"
              disabled
              className="w-full"
            >
              قيد التطوير
            </CopticButton>
          </GlassCard>
        </div>

        {/* Upcoming Events & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content - Left */}
          <div className="lg:col-span-2 space-y-6">
            {/* Upcoming Events */}
            <GlassCard variant="default">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-display font-semibold text-xl text-cream">الأحداث القادمة</h2>
                <CopticButton variant="text">عرض الكل</CopticButton>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-start p-4 bg-navy-light/20 rounded-lg border-l-4 border-l-gold-primary">
                  <div>
                    <div className="text-cream font-body font-semibold">خدمة الأحد</div>
                    <div className="text-text-muted font-body text-sm">غداً في الساعة 10:00 صباحاً</div>
                  </div>
                  <div className="text-gold-primary text-sm font-bold">خلال يوم</div>
                </div>
                <div className="flex justify-between items-start p-4 bg-navy-light/20 rounded-lg border-l-4 border-l-gold-primary">
                  <div>
                    <div className="text-cream font-body font-semibold">اجتماع الشباب</div>
                    <div className="text-text-muted font-body text-sm">الأربعاء في الساعة 7:00 مساءً</div>
                  </div>
                  <div className="text-gold-primary text-sm font-bold">خلال 4 أيام</div>
                </div>
              </div>
            </GlassCard>

            {/* Recent Registrations */}
            <GlassCard variant="default">
              <h2 className="font-display font-semibold text-xl text-cream mb-4">التسجيلات الحديثة</h2>
              <DataTable
                columns={[
                  { key: 'name', label: 'الاسم' },
                  { key: 'email', label: 'البريد الإلكتروني' },
                  { key: 'date', label: 'تاريخ التسجيل' },
                ]}
                data={[
                  { name: 'جون كمال', email: 'john@example.com', date: 'اليوم' },
                  { name: 'ماري جرجس', email: 'mary@example.com', date: 'أمس' },
                  { name: 'مينا يوسف', email: 'mina@example.com', date: 'منذ يومين' },
                ]}
              />
            </GlassCard>
          </div>

          {/* Sidebar - Right */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <GlassCard variant="default">
              <h2 className="font-display font-semibold text-lg text-cream mb-4">الإجراءات السريعة</h2>
              <div className="space-y-2 flex flex-col">
                <CopticButton variant="primary" className="w-full">إضافة عضو</CopticButton>
                <CopticButton variant="secondary" className="w-full">عرض التقارير</CopticButton>
                <CopticButton variant="secondary" className="w-full">الإعدادات</CopticButton>
              </div>
            </GlassCard>

            {/* Community Stats */}
            <GlassCard variant="with-top-border">
              <h3 className="font-display font-semibold text-gold-accent text-sm uppercase mb-3">
                إحصائيات المجتمع
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between pb-2 border-b border-gold-primary/20">
                  <span className="text-text-muted font-body">النشط اليوم</span>
                  <span className="text-cream font-body font-semibold">87</span>
                </div>
                <div className="flex justify-between pb-2 border-b border-gold-primary/20">
                  <span className="text-text-muted font-body">هذا الأسبوع</span>
                  <span className="text-cream font-body font-semibold">234</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted font-body">هذا الشهر</span>
                  <span className="text-cream font-body font-semibold">248</span>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </main>
    </div>
  );
}
