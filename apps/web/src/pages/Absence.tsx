import { useState, useEffect } from 'react'
import { GlassCard, GlassButton } from '../components/ui'
import { useAttendanceStore } from '../store/attendance'
import { useSettingsStore } from '../store/settings'
import { exportAbsenceReportToExcel } from '../lib/excel'
import { formatDate } from '../lib/utils'

export default function AbsencePage() {
  const {
    fetchAttendanceDates,
    attendanceDates,
    fetchAbsentChildren,
    absentChildren,
    fetchAbsentChildrenByClass,
  } = useAttendanceStore()

  const { fetchSettings, settings } = useSettingsStore()

  const [selectedDate, setSelectedDate] = useState(formatDate(new Date()))
  const [showServerModal, setShowServerModal] = useState(false)
  const [selectedClass, setSelectedClass] = useState('الصف الأول')
  const [classAbsentChildren, setClassAbsentChildren] = useState<any[]>([])

  useEffect(() => {
    fetchAttendanceDates()
    fetchSettings()
    handleDateChange(selectedDate)
  }, [])

  const handleDateChange = async (date: string) => {
    setSelectedDate(date)
    await fetchAbsentChildren(date)
  }

  const handleClassFilter = async (className: string) => {
    setSelectedClass(className)
    const absent = await fetchAbsentChildrenByClass(selectedDate, className)
    setClassAbsentChildren(absent)
  }

  const classes = ['الصف الأول', 'الصف الثاني', 'الصف الثالث']

  const handleExportAbsence = () => {
    if (absentChildren.length === 0) {
      alert('لا توجد حالات غياب للتصدير')
      return
    }
    exportAbsenceReportToExcel(
      absentChildren,
      selectedDate,
      `غياب_${selectedDate}.xlsx`,
    )
  }

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gradient mb-2">
            📋 تقرير الغياب
          </h1>
          <p className="text-glass-muted">
            عرض وإدارة حالات الغياب وتوزيع المتابعة
          </p>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Left Panel */}
          <div className="space-y-6">
            {/* Date Selector */}
            <GlassCard>
              <h2 className="text-lg font-semibold text-glass-text mb-4">
                اختيار التاريخ
              </h2>
              <select
                value={selectedDate}
                onChange={(e) => handleDateChange(e.target.value)}
                className="glass-select w-full mb-4"
              >
                <option value="">اختر تاريخ...</option>
                {attendanceDates.map((date) => (
                  <option key={date} value={date}>
                    {date}
                  </option>
                ))}
              </select>

              <GlassButton
                variant="secondary"
                fullWidth
                onClick={() => handleDateChange(formatDate(new Date()))}
              >
                اليوم
              </GlassButton>
            </GlassCard>

            {/* Stats */}
            <GlassCard>
              <h2 className="text-lg font-semibold text-glass-text mb-4">
                الإحصائيات
              </h2>
              <div className="space-y-3">
                <div className="glass p-3 rounded-lg">
                  <p className="text-sm text-glass-muted">إجمالي الغائبين</p>
                  <p className="text-2xl font-bold text-glass-text">
                    {absentChildren.length}
                  </p>
                </div>
                <div className="glass p-3 rounded-lg">
                  <p className="text-sm text-glass-muted">نسبة الغياب</p>
                  <p className="text-2xl font-bold text-glass-text">
                    {absentChildren.length > 0
                      ? `${Math.round((absentChildren.length / 50) * 100)}%`
                      : '0%'}
                  </p>
                </div>
              </div>
            </GlassCard>

            {/* Actions */}
            <GlassButton
              variant="primary"
              fullWidth
              onClick={() => setShowServerModal(true)}
              disabled={absentChildren.length === 0}
            >
              توزيع على الخدام
            </GlassButton>

            <GlassButton
              variant="secondary"
              fullWidth
              onClick={handleExportAbsence}
              disabled={absentChildren.length === 0}
            >
              📤 تصدير Excel
            </GlassButton>

            {/* Service Days Filter */}
            <GlassCard>
              <h2 className="text-lg font-semibold text-glass-text mb-4">
                الخيارات
              </h2>
              <label className="flex items-center gap-3 text-glass-text cursor-pointer">
                <input
                  type="checkbox"
                  defaultChecked
                  className="rounded w-4 h-4"
                />
                <span className="text-sm">أيام الخدمة فقط</span>
              </label>
            </GlassCard>
          </div>

          {/* Right Panel - Absence Tables */}
          <div className="col-span-2">
            <GlassCard>
              <div className="flex gap-2 mb-6 flex-wrap">
                {classes.map((className) => (
                  <button
                    key={className}
                    onClick={() => handleClassFilter(className)}
                    className={`px-4 py-2 rounded-lg transition-colors font-medium text-sm ${
                      selectedClass === className
                        ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                        : 'glass text-glass-text hover:bg-blue-500/10'
                    }`}
                  >
                    {className}
                  </button>
                ))}
              </div>

              {/* Absence Table */}
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
                        المنطقة
                      </th>
                      <th className="px-4 py-3 text-right font-semibold text-glass-text">
                        الهاتف
                      </th>
                      <th className="px-4 py-3 text-right font-semibold text-glass-text">
                        الإجراء
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {(classAbsentChildren.length > 0
                      ? classAbsentChildren
                      : absentChildren
                    ).map((child) => (
                      <tr
                        key={child.code}
                        className="border-b border-glass-border/50 hover:bg-blue-500/5 transition-colors"
                      >
                        <td className="px-4 py-3 text-glass-text">
                          {child.code}
                        </td>
                        <td className="px-4 py-3 text-glass-text">
                          {child.name}
                        </td>
                        <td className="px-4 py-3 text-glass-muted">
                          {child.region}
                        </td>
                        <td className="px-4 py-3 text-glass-muted">
                          {child.childMobile}
                        </td>
                        <td className="px-4 py-3">
                          <button className="px-3 py-1 rounded bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 transition-colors text-xs">
                            عرض
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {(classAbsentChildren.length === 0 &&
                  absentChildren.length === 0) && (
                  <p className="text-center text-glass-muted py-8">
                    لا توجد حالات غياب
                  </p>
                )}
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Server Assignment Modal */}
        {showServerModal && (
          <div className="modal-overlay">
            <div className="modal-content max-w-2xl">
              <div className="modal-header">
                <h2 className="modal-title">توزيع الغائبين على الخدام</h2>
                <button
                  className="modal-close"
                  onClick={() => setShowServerModal(false)}
                >
                  ✕
                </button>
              </div>

              <div className="modal-body">
                <p className="text-glass-muted mb-4">
                  {absentChildren.length} طفل/ة غائب/ة سيتم توزيعهم على الخدام
                </p>

                <div className="space-y-3">
                  <div className="glass p-4 rounded-lg">
                    <p className="font-semibold text-glass-text mb-2">
                      خادم 1 - أحمد
                    </p>
                    <p className="text-sm text-glass-muted">
                      {Math.ceil(absentChildren.length / 3)} أطفال
                    </p>
                  </div>
                  <div className="glass p-4 rounded-lg">
                    <p className="font-semibold text-glass-text mb-2">
                      خادم 2 - فاطمة
                    </p>
                    <p className="text-sm text-glass-muted">
                      {Math.ceil(absentChildren.length / 3)} أطفال
                    </p>
                  </div>
                  <div className="glass p-4 rounded-lg">
                    <p className="font-semibold text-glass-text mb-2">
                      خادم 3 - محمود
                    </p>
                    <p className="text-sm text-glass-muted">
                      {absentChildren.length - Math.ceil(absentChildren.length / 3) * 2} أطفال
                    </p>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <GlassButton
                  variant="secondary"
                  onClick={() => setShowServerModal(false)}
                >
                  إلغاء
                </GlassButton>
                <GlassButton
                  variant="success"
                  onClick={() => {
                    setShowServerModal(false)
                  }}
                >
                  تأكيد التوزيع
                </GlassButton>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
