import { useState, useEffect } from 'react'
import { GlassCard, GlassButton, GlassInput, StatCard } from '../components/ui'
import { useAttendanceStore } from '../store/attendance'
import { useChildrenStore } from '../store/children'
import { formatTime } from '../lib/utils'

export default function RegistrationPage() {
  const {
    currentSessionDate,
    currentSessionAttendance,
    startSession,
    endSession,
    recordAttendance,
  } = useAttendanceStore()

  const { children, fetchChildren } = useChildrenStore()

  const [codeInput, setCodeInput] = useState('')
  const [selectedChild, setSelectedChild] = useState<any | null>(null)
  const [sessionStartTime] = useState(Date.now())
  const [filteredChildren, setFilteredChildren] = useState<any[]>([])

  useEffect(() => {
    fetchChildren()
    if (!currentSessionDate) {
      startSession()
    }
  }, [])

  // Handle code input - search for child
  const handleCodeSearch = () => {
    if (!codeInput.trim()) return

    const found = children.find(
      (c) => c.code === codeInput.trim() || c.name.includes(codeInput.trim()),
    )

    if (found) {
      setSelectedChild(found)
      setCodeInput('')
    }
  }

  // Register attendance
  const handleRegister = async () => {
    if (!selectedChild) return

    try {
      const now = new Date()
      const time = `${String(now.getHours()).padStart(2, '0')}:${String(
        now.getMinutes(),
      ).padStart(2, '0')}`

      await recordAttendance(selectedChild.code, time)
      setSelectedChild(null)
    } catch (err) {
      console.error('Failed to register attendance:', err)
    }
  }

  // Handle end session
  const handleEndSession = async () => {
    if (window.confirm('هل تريد بالفعل إنهاء الجلسة؟')) {
      await endSession()
    }
  }

  const registeredCount = Object.keys(currentSessionAttendance).length
  const totalChildren = children.length
  const remainingCount = totalChildren - registeredCount
  const elapsedMinutes = Math.floor((Date.now() - sessionStartTime) / 60000)

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gradient mb-2">
            📝 التسجيل اليومي
          </h1>
          <p className="text-glass-muted">
            {currentSessionDate || 'جاري تحميل التاريخ...'}
          </p>
        </div>

        {/* Session Stats */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <StatCard
            icon="👥"
            label="إجمالي الأطفال"
            value={totalChildren}
            color="primary"
          />
          <StatCard
            icon="✓"
            label="مسجلين اليوم"
            value={registeredCount}
            color="success"
          />
          <StatCard
            icon="⏳"
            label="المتبقي"
            value={remainingCount}
            color="warning"
          />
          <StatCard
            icon="⏱️"
            label="الوقت المنقضي"
            value={`${elapsedMinutes}د`}
            color="primary"
          />
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Registration Form */}
          <div className="col-span-2 space-y-6">
            <GlassCard>
              <h2 className="text-xl font-semibold text-glass-text mb-4">
                تسجيل الحضور
              </h2>

              <div className="space-y-4">
                <div className="flex gap-2">
                  <GlassInput
                    label="رقم أو اسم الطفل"
                    value={codeInput}
                    onChange={(e) => setCodeInput(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') handleCodeSearch()
                    }}
                    placeholder="أدخل الرقم أو الاسم"
                    className="flex-1"
                  />
                  <div className="flex items-end">
                    <GlassButton
                      variant="primary"
                      onClick={handleCodeSearch}
                    >
                      بحث
                    </GlassButton>
                  </div>
                </div>

                {/* Child search results */}
                {codeInput && filteredChildren.length > 0 && (
                  <div className="glass p-3 rounded-lg max-h-48 overflow-y-auto">
                    {filteredChildren.map((child) => (
                      <button
                        key={child.code}
                        onClick={() => {
                          setSelectedChild(child)
                          setCodeInput('')
                        }}
                        className="w-full text-right p-2 hover:bg-blue-500/10 rounded transition-colors"
                      >
                        <p className="font-medium text-glass-text">
                          {child.name}
                        </p>
                        <p className="text-sm text-glass-muted">{child.code}</p>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </GlassCard>

            {/* Selected Child Info */}
            {selectedChild && (
              <GlassCard className="bg-gradient-to-br from-blue-600/10 to-indigo-600/10 border border-blue-500/30">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-glass-text">
                      {selectedChild.name}
                    </h3>
                    <p className="text-sm text-glass-muted">
                      {selectedChild.code} - {selectedChild.class}
                    </p>
                  </div>
                  <button
                    onClick={() => setSelectedChild(null)}
                    className="text-glass-muted hover:text-glass-text"
                  >
                    ✕
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                  <div>
                    <p className="text-glass-muted">المنطقة</p>
                    <p className="text-glass-text font-medium">
                      {selectedChild.region || 'غير محدد'}
                    </p>
                  </div>
                  <div>
                    <p className="text-glass-muted">المدرسة</p>
                    <p className="text-glass-text font-medium">
                      {selectedChild.school || 'غير محدد'}
                    </p>
                  </div>
                </div>

                <div className="space-y-2">
                  {!currentSessionAttendance[selectedChild.code] ? (
                    <GlassButton
                      variant="success"
                      fullWidth
                      onClick={handleRegister}
                    >
                      ✓ تسجيل الحضور
                    </GlassButton>
                  ) : (
                    <div className="p-3 rounded-lg bg-green-500/20 border border-green-500/50 text-center">
                      <p className="text-green-300 font-medium">
                        ✓ تم التسجيل الساعة{' '}
                        {currentSessionAttendance[selectedChild.code]}
                      </p>
                    </div>
                  )}
                </div>
              </GlassCard>
            )}

            {/* End Session Button */}
            <GlassButton
              variant="danger"
              fullWidth
              onClick={handleEndSession}
              disabled={registeredCount === 0}
            >
              إنهاء الجلسة
            </GlassButton>
          </div>

          {/* Attendance List */}
          <div>
            <GlassCard>
              <h2 className="text-lg font-semibold text-glass-text mb-4">
                المسجلين اليوم ({registeredCount})
              </h2>

              <div className="space-y-2 max-h-96 overflow-y-auto">
                {Object.entries(currentSessionAttendance).length === 0 ? (
                  <p className="text-glass-muted text-sm text-center py-4">
                    لم يتم تسجيل أحد بعد
                  </p>
                ) : (
                  Object.entries(currentSessionAttendance).map(
                    ([code, time]) => {
                      const child = children.find((c) => c.code === code)
                      return (
                        <div
                          key={code}
                          className="glass p-3 rounded-lg text-sm"
                        >
                          <p className="font-medium text-glass-text">
                            {child?.name || code}
                          </p>
                          <p className="text-glass-muted text-xs">
                            {code} • {time}
                          </p>
                        </div>
                      )
                    },
                  )
                )}
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  )
}
