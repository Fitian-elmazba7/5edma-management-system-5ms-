import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'

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
    <div className="min-h-screen bg-glass-bg flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="glass-card">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gradient mb-2">
              نظام الخدمة
            </h1>
            <p className="text-glass-muted">إدارة الحضور والغياب</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                البريد الإلكتروني
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="glass-input"
                placeholder="أدخل بريدك الإلكتروني"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                كلمة المرور
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="glass-input"
                placeholder="أدخل كلمة المرور"
                disabled={loading}
              />
            </div>

            {(error || localError) && (
              <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50">
                <p className="text-red-300 text-sm">{error || localError}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full glass-button-primary"
            >
              {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            </button>
          </form>

          <p className="text-center text-glass-muted text-sm mt-6">
            نظام الكنيسة القبطية الأرثوذكسية
          </p>
        </div>
      </div>
    </div>
  )
}
