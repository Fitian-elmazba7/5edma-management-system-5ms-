import { useState, useEffect } from 'react'
import { GlassCard, GlassButton } from '../components/ui'
import { formatDate } from '../lib/utils'

export default function ComparisonReportPage() {
  const [startDate, setStartDate] = useState(
    formatDate(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)),
  )
  const [endDate, setEndDate] = useState(formatDate(new Date()))
  const [selectedClass, setSelectedClass] = useState('الكل')
  const [showServiceDaysOnly, setShowServiceDaysOnly] = useState(false)

  const classes = ['الكل', 'الصف الأول', 'الصف الثاني', 'الصف الثالث']

  // Mock comparison data
  const mockComparisonData = [
    {
      code: '101',
      name: 'أحمد محمود',
      class: 'الصف الأول',
      totalDays: 7,
      presentDays: 6,
      absentDays: 1,
      attendanceRate: '86%',
    },
    {
      code: '102',
      name: 'فاطمة علي',
      class: 'الصف الثاني',
      totalDays: 7,
      presentDays: 7,
      absentDays: 0,
      attendanceRate: '100%',
    },
    {
      code: '103',
      name: 'محمد الحسن',
      class: 'الصف الأول',
      totalDays: 7,
      presentDays: 5,
      absentDays: 2,
      attendanceRate: '71%',
    },
  ]

  const filteredData =
    selectedClass === 'الكل'
      ? mockComparisonData
      : mockComparisonData.filter((child) => child.class === selectedClass)

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
              📊 تقارير المقارنة
            </h1>
            <p className="text-glass-muted">
              مقارنة الحضور عبر فترة زمنية محددة
            </p>
          </div>
          <GlassButton variant="primary" onClick={handleExportToExcel}>
            📊 تصدير Excel
          </GlassButton>
        </div>

        {/* Filters */}
        <GlassCard className="mb-6">
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                من التاريخ
              </label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="glass-input w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                إلى التاريخ
              </label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="glass-input w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                الصف
              </label>
              <select
                value={selectedClass}
                onChange={(e) => setSelectedClass(e.target.value)}
                className="glass-select w-full"
              >
                {classes.map((className) => (
                  <option key={className} value={className}>
                    {className}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-glass-text mb-2">
                الخيارات
              </label>
              <label className="flex items-center gap-2 text-glass-text cursor-pointer">
                <input
                  type="checkbox"
                  checked={showServiceDaysOnly}
                  onChange={(e) => setShowServiceDaysOnly(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm">أيام الخدمة فقط</span>
              </label>
            </div>
          </div>
        </GlassCard>

        {/* Comparison Table */}
        <GlassCard>
          <h2 className="text-xl font-semibold text-glass-text mb-6">
            المقارنة من {startDate} إلى {endDate}
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
                  <th className="px-4 py-3 text-center font-semibold text-glass-text">
                    إجمالي الأيام
                  </th>
                  <th className="px-4 py-3 text-center font-semibold text-glass-text">
                    حاضر
                  </th>
                  <th className="px-4 py-3 text-center font-semibold text-glass-text">
                    غائب
                  </th>
                  <th className="px-4 py-3 text-center font-semibold text-glass-text">
                    النسبة
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((child) => (
                  <tr
                    key={child.code}
                    className="border-b border-glass-border/50 hover:bg-blue-500/5"
                  >
                    <td className="px-4 py-3 text-glass-text">{child.code}</td>
                    <td className="px-4 py-3 text-glass-text">{child.name}</td>
                    <td className="px-4 py-3 text-glass-muted">{child.class}</td>
                    <td className="px-4 py-3 text-center text-glass-text">
                      {child.totalDays}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="px-3 py-1 rounded bg-green-500/20 text-green-300 text-xs">
                        {child.presentDays}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="px-3 py-1 rounded bg-red-500/20 text-red-300 text-xs">
                        {child.absentDays}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center font-bold">
                      <span
                        className={`px-3 py-1 rounded text-xs ${
                          parseInt(child.attendanceRate) >= 80
                            ? 'bg-green-500/20 text-green-300'
                            : parseInt(child.attendanceRate) >= 60
                              ? 'bg-amber-500/20 text-amber-300'
                              : 'bg-red-500/20 text-red-300'
                        }`}
                      >
                        {child.attendanceRate}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredData.length === 0 && (
            <p className="text-center text-glass-muted py-8">
              لا توجد بيانات للمقارنة
            </p>
          )}
        </GlassCard>
      </div>
    </div>
  )
}
