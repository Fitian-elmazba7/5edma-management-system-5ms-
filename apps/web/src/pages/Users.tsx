import { useState } from 'react'
import { useAuthStore } from '../store/auth'
import { Navigate } from 'react-router-dom'
import { GlassCard, GlassButton, GlassInput } from '../components/ui'
import { UserRole } from '@5edma/shared'

export default function UsersPage() {
  const { user } = useAuthStore()
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [inviteEmail, setInviteEmail] = useState('')
  const [inviteRole, setInviteRole] = useState<UserRole>('viewer')

  // Only admins can access this page
  if (user?.role !== 'admin') {
    return <Navigate to="/" replace />
  }

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement Firebase user invitation
    console.log('Invite user:', inviteEmail, inviteRole)
    setInviteEmail('')
    setShowInviteModal(false)
  }

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gradient">إدارة المستخدمين</h1>
          <GlassButton
            variant="primary"
            onClick={() => setShowInviteModal(true)}
          >
            دعوة مستخدم جديد
          </GlassButton>
        </div>

        {/* Placeholder content */}
        <GlassCard className="mb-8">
          <h2 className="text-xl font-semibold text-glass-text mb-4">
            قائمة المستخدمين
          </h2>
          <p className="text-glass-muted">
            جاري تطوير قائمة المستخدمين - سيتم إتاحتها في المرحلة القادمة
          </p>
        </GlassCard>

        {/* Invite Modal */}
        {showInviteModal && (
          <div className="modal-overlay">
            <div className="modal-content max-w-md">
              <div className="modal-header">
                <h2 className="modal-title">دعوة مستخدم جديد</h2>
                <button
                  className="modal-close"
                  onClick={() => setShowInviteModal(false)}
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleInvite} className="modal-body space-y-4">
                <GlassInput
                  label="البريد الإلكتروني"
                  type="email"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="أدخل البريد الإلكتروني"
                  required
                />

                <div>
                  <label className="block text-sm font-medium text-glass-text mb-2">
                    الصلاحيات
                  </label>
                  <select
                    value={inviteRole}
                    onChange={(e) => setInviteRole(e.target.value as UserRole)}
                    className="glass-select w-full"
                  >
                    <option value="viewer">مشاهد</option>
                    <option value="user">مستخدم</option>
                    <option value="servant">خادم</option>
                    <option value="admin">مسؤول</option>
                  </select>
                </div>

                <div className="modal-footer">
                  <GlassButton
                    variant="secondary"
                    onClick={() => setShowInviteModal(false)}
                  >
                    إلغاء
                  </GlassButton>
                  <GlassButton type="submit" variant="primary">
                    إرسال الدعوة
                  </GlassButton>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
