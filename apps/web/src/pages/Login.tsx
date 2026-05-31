import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'
import { GlassInput, GlassButton } from '../components/ui'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login, error, loading } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [localError, setLocalError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLocalError('')

    if (!email || !password) {
      setLocalError('يرجى إدخال البريد الإلكتروني وكلمة المرور')
      return
    }

    try {
      await login(email, password)
      navigate('/')
    } catch (err) {
      setLocalError(
        err instanceof Error ? err.message : 'حدث خطأ في تسجيل الدخول',
      )
    }
  }

  return (
    <div className="min-h-screen bg-glass-bg flex items-center justify-center p-4 relative overflow-hidden">
      {/* Decorative gradient blobs */}
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-600/20 to-indigo-600/20 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-600/20 to-blue-600/20 rounded-full blur-3xl"></div>

      <div className="w-full max-w-md relative z-10">
        <div className="glass-card">
          <div className="text-center mb-8">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
              <span className="text-2xl">⛪</span>
            </div>
            <h1 className="text-3xl font-bold text-gradient mb-2">
              نظام الخدمة
            </h1>
            <p className="text-glass-muted">إدارة الحضور والغياب</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <GlassInput
              label="البريد الإلكتروني"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="أدخل بريدك الإلكتروني"
              disabled={loading}
              error={localError ? 'البريد مطلوب' : undefined}
            />

            <GlassInput
              label="كلمة المرور"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="أدخل كلمة المرور"
              disabled={loading}
              error={localError ? 'كلمة المرور مطلوبة' : undefined}
            />

            {(error || localError) && (
              <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50">
                <p className="text-red-300 text-sm">{error || localError}</p>
              </div>
            )}

            <GlassButton
              type="submit"
              variant="primary"
              fullWidth
              loading={loading}
              disabled={loading}
            >
              تسجيل الدخول
            </GlassButton>
          </form>

          <div className="mt-8 pt-6 border-t border-glass-border">
            <p className="text-center text-glass-muted text-xs mb-3">
              للاختبار استخدم:
            </p>
            <div className="space-y-1 text-xs text-glass-muted text-center">
              <p>البريد: demo@example.com</p>
              <p>كلمة المرور: demo123</p>
            </div>
          </div>

          <p className="text-center text-glass-muted text-xs mt-6">
            © الكنيسة القبطية الأرثوذكسية
          </p>
        </div>
      </div>
    </div>
  )
}
