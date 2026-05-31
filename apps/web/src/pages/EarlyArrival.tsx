import { useState, useEffect } from 'react'
import { GlassCard, GlassButton, GlassInput } from '../components/ui'
import { useSettingsStore } from '../store/settings'
import { formatDate } from '../lib/utils'

export default function EarlyArrivalPage() {
  const { fetchSettings, updateServiceTime, settings } = useSettingsStore()
  const [selectedDate, setSelectedDate] = useState(formatDate(new Date()))
  const [showSettingsModal, setShowSettingsModal] = useState(false)
  const [serviceTime, setServiceTime] = useState('19:00')

  useEffect(() => {
    fetchSettings()
  }, [])

  useEffect(() => {
    if (settings) {
      setServiceTime(settings.serviceTime)
    }
  }, [settings])

  const handleUpdateServiceTime = async () => {
    await updateServiceTime(serviceTime)
    setShowSettingsModal(false)
  }

  const mockEarlyArrivals = [
    {
      code: '101',
      name: 'أحمد محمود',
      class: 'الصف الأول',
      arrivalTime: '18:45',
      earlyBy: '15 دقيقة',
    },
    {
      code: '102',
      name: 'فاطمة علي',
      class: 'الصف الثاني',
      arrivalTime: '18:50',
      earlyBy: '10 دقائق',
    },
  ]

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gradient mb-2">
              ⏰ الحضور المبكر
            </h1>
            <p className="text-glass-muted">
              عرض الأطفال الذين يصلون قبل موعد الخدمة
            </p>
          </div>
          <GlassButton
            variant="secondary"
            onClick={() => setShowSettingsModal(true)}
          >
            ⚙️ إعدادات الخدمة
          </GlassButton>
        </div>

        {/* Date & Settings Info */}
        <GlassCard className="mb-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                التاريخ
              </label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="glass-input w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                موعد الخدمة
              </label>
              <div className="glass p-3 rounded-lg">
                <p className="text-2xl font-bold text-glass-primary">
                  {settings?.serviceTime}
                </p>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Early Arrivals List */}
        <GlassCard>
          <h2 className="text-xl font-semibold text-glass-text mb-6">
            الحضور المبكر ({mockEarlyArrivals.length})
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-glass-border">
                  <th className="px-4 py-3 text-right font-semibold text-glass-text">
                    الرقم
                  </th>
                  <th className="px-4 py-3 text-right font-semibold text-glass-text">
                    الاسم
                  </th>
                  <th className="px-4 py-3 text-right font-semibold text-glass-text">
                    الصف
                  </th>
                  <th className="px-4 py-3 text-right font-semibold text-glass-text">
                    وقت الوصول
                  </th>
                  <th className="px-4 py-3 text-right font-semibold text-glass-text">
                    مبكر بـ
                  </th>
                </tr>
              </thead>
              <tbody>
                {mockEarlyArrivals.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-8 text-center text-glass-muted">
                      لا توجد حالات حضور مبكر
                    </td>
                  </tr>
                ) : (
                  mockEarlyArrivals.map((arrival) => (
                    <tr
                      key={arrival.code}
                      className="border-b border-glass-border/50 hover:bg-blue-500/5"
                    >
                      <td className="px-4 py-3 text-glass-text">
                        {arrival.code}
                      </td>
                      <td className="px-4 py-3 text-glass-text">
                        {arrival.name}
                      </td>
                      <td className="px-4 py-3 text-glass-muted">
                        {arrival.class}
                      </td>
                      <td className="px-4 py-3 text-glass-text">
                        {arrival.arrivalTime}
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-3 py-1 rounded bg-amber-500/20 text-amber-300 text-xs">
                          {arrival.earlyBy}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </GlassCard>

        {/* Settings Modal */}
        {showSettingsModal && (
          <div className="modal-overlay">
            <div className="modal-content max-w-md">
              <div className="modal-header">
                <h2 className="modal-title">إعدادات الخدمة</h2>
                <button
                  className="modal-close"
                  onClick={() => setShowSettingsModal(false)}
                >
                  ✕
                </button>
              </div>

              <div className="modal-body space-y-4">
                <div>
                  <label className="block text-sm font-medium text-glass-text mb-2">
                    موعد الخدمة الرسمي
                  </label>
                  <input
                    type="time"
                    value={serviceTime}
                    onChange={(e) => setServiceTime(e.target.value)}
                    className="glass-input w-full"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <GlassButton
                  variant="secondary"
                  onClick={() => setShowSettingsModal(false)}
                >
                  إلغاء
                </GlassButton>
                <GlassButton variant="primary" onClick={handleUpdateServiceTime}>
                  حفظ التغييرات
                </GlassButton>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
