import { useState, useEffect } from 'react'
import { GlassCard, GlassButton } from '../components/ui'
import { useAttendanceStore } from '../store/attendance'
import { useChildrenStore } from '../store/children'
import { formatDate } from '../lib/utils'

export default function AttendanceReportPage() {
  const { fetchAttendanceDates, attendanceDates, selectedDateStats, fetchAttendanceStats } =
    useAttendanceStore()
  const { children } = useChildrenStore()

  const [selectedDate, setSelectedDate] = useState(formatDate(new Date()))
  const [selectedClass, setSelectedClass] = useState('الكل')
  const [presentChildren, setPresentChildren] = useState<any[]>([])

  useEffect(() => {
    fetchAttendanceDates()
    handleDateChange(selectedDate)
  }, [])

  const handleDateChange = async (date: string) => {
    setSelectedDate(date)
    await fetchAttendanceStats(date)
  }

  const classes = ['الكل', 'الصف الأول', 'الصف الثاني', 'الصف الثالث']

  const filteredPresentChildren =
    selectedClass === 'الكل'
      ? presentChildren
      : presentChildren.filter((c) => c.class === selectedClass)

  const handleExportToExcel = () => {
    alert('جاري تطوير خاصية التصدير إلى Excel')
  }

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gradient mb-2">
              📋 تقرير الحضور
            </h1>
            <p className="text-glass-muted">
              عرض تفاصيل الحضور لتاريخ معين
            </p>
          </div>
          <GlassButton
            variant="primary"
            onClick={handleExportToExcel}
          >
            📊 تصدير Excel
          </GlassButton>
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
                className="glass-select w-full"
              >
                <option value="">اختر تاريخ...</option>
                {attendanceDates.map((date) => (
                  <option key={date} value={date}>
                    {date}
                  </option>
                ))}
              </select>
            </GlassCard>

            {/* Stats */}
            {selectedDateStats && (
              <GlassCard>
                <h2 className="text-lg font-semibold text-glass-text mb-4">
                  الإحصائيات
                </h2>
                <div className="space-y-3">
                  <div className="glass p-3 rounded-lg">
                    <p className="text-sm text-glass-muted">إجمالي الأطفال</p>
                    <p className="text-2xl font-bold text-glass-text">
                      {selectedDateStats.total}
                    </p>
                  </div>
                  <div className="glass p-3 rounded-lg">
                    <p className="text-sm text-glass-muted">الحاضرين</p>
                    <p className="text-2xl font-bold text-green-300">
                      {selectedDateStats.present}
                    </p>
                  </div>
                  <div className="glass p-3 rounded-lg">
                    <p className="text-sm text-glass-muted">الغائبين</p>
                    <p className="text-2xl font-bold text-red-300">
                      {selectedDateStats.absent}
                    </p>
                  </div>
                  <div className="glass p-3 rounded-lg">
                    <p className="text-sm text-glass-muted">نسبة الحضور</p>
                    <p className="text-2xl font-bold text-blue-300">
                      {selectedDateStats.attendanceRate}%
                    </p>
                  </div>
                </div>
              </GlassCard>
            )}
          </div>

          {/* Right Panel - Present Children List */}
          <div className="col-span-2">
            <GlassCard>
              <div className="flex gap-2 mb-6 flex-wrap">
                {classes.map((className) => (
                  <button
                    key={className}
                    onClick={() => setSelectedClass(className)}
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

              {/* Present Children Table */}
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
                        المدرسة
                      </th>
                      <th className="px-4 py-3 text-right font-semibold text-glass-text">
                        الموبايل
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredPresentChildren.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="px-4 py-8 text-center text-glass-muted">
                          لا توجد بيانات حضور
                        </td>
                      </tr>
                    ) : (
                      filteredPresentChildren.map((child) => (
                        <tr
                          key={child.code}
                          className="border-b border-glass-border/50 hover:bg-blue-500/5"
                        >
                          <td className="px-4 py-3 text-glass-text">
                            {child.code}
                          </td>
                          <td className="px-4 py-3 text-glass-text">
                            {child.name}
                          </td>
                          <td className="px-4 py-3 text-glass-muted">
                            {child.class}
                          </td>
                          <td className="px-4 py-3 text-glass-muted">
                            {child.school}
                          </td>
                          <td className="px-4 py-3 text-glass-muted">
                            {child.childMobile}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  )
}
