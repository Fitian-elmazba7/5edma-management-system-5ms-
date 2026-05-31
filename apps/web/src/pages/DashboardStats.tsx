import { useState, useEffect } from 'react'
import {
  PieChart,
  Pie,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import { GlassCard, GlassButton, GlassInput, StatCard } from '../components/ui'
import { useChildrenStore } from '../store/children'
import { useAttendanceStore } from '../store/attendance'
import { formatDate, getArabicMonth } from '../lib/utils'

export default function DashboardStatsPage() {
  const { children, fetchChildren } = useChildrenStore()
  const { fetchAttendanceStats, selectedDateStats, fetchAbsentChildren } =
    useAttendanceStore()

  const [selectedDate, setSelectedDate] = useState(formatDate(new Date()))
  const [attendanceHistory, setAttendanceHistory] = useState<any[]>([])

  useEffect(() => {
    fetchChildren()
    handleDateChange(selectedDate)
  }, [])

  const handleDateChange = async (date: string) => {
    setSelectedDate(date)
    await fetchAttendanceStats(date)
    await fetchAbsentChildren(date)

    // Generate mock history data for chart (in real app, fetch from DB)
    const history = []
    const now = new Date(date)
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now)
      d.setDate(d.getDate() - i)
      history.push({
        date: d.toLocaleDateString('ar-EG', { month: 'short', day: 'numeric' }),
        present: Math.floor(Math.random() * (children.length - 10) + 10),
        absent: Math.floor(Math.random() * 10 + 2),
      })
    }
    setAttendanceHistory(history)
  }

  const pieData = selectedDateStats
    ? [
        {
          name: 'حضور',
          value: selectedDateStats.present,
          fill: '#22c55e',
        },
        {
          name: 'غياب',
          value: selectedDateStats.absent,
          fill: '#ef4444',
        },
      ]
    : []

  const classData = selectedDateStats
    ? Object.entries(selectedDateStats.byClass).map(([className, stats]) => ({
        name: className,
        present: stats.present,
        absent: stats.absent,
      }))
    : []

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gradient mb-2">
            📊 لوحة البيانات
          </h1>
          <p className="text-glass-muted">إحصائيات وتقارير الحضور والغياب</p>
        </div>

        {/* Date Selector */}
        <GlassCard className="mb-8">
          <h2 className="text-lg font-semibold text-glass-text mb-4">
            اختيار التاريخ
          </h2>
          <div className="flex gap-4">
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => handleDateChange(e.target.value)}
              className="glass-input flex-1"
            />
            <GlassButton
              variant="secondary"
              onClick={() => handleDateChange(formatDate(new Date()))}
            >
              اليوم
            </GlassButton>
          </div>
        </GlassCard>

        {/* Stats Grid */}
        {selectedDateStats && (
          <>
            <div className="grid grid-cols-4 gap-4 mb-8">
              <StatCard
                icon="👥"
                label="إجمالي الأطفال"
                value={selectedDateStats.total}
                color="primary"
              />
              <StatCard
                icon="✓"
                label="حاضرين"
                value={selectedDateStats.present}
                color="success"
              />
              <StatCard
                icon="✕"
                label="غائبين"
                value={selectedDateStats.absent}
                color="danger"
              />
              <StatCard
                icon="📈"
                label="نسبة الحضور"
                value={`${selectedDateStats.attendanceRate}%`}
                color="primary"
              />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-2 gap-6 mb-8">
              {/* Pie Chart */}
              <GlassCard>
                <h3 className="text-lg font-semibold text-glass-text mb-4">
                  توزيع الحضور والغياب
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        `${name}: ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </GlassCard>

              {/* Bar Chart - By Class */}
              <GlassCard>
                <h3 className="text-lg font-semibold text-glass-text mb-4">
                  الحضور حسب الصف
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={classData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="name" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(8,14,26,0.7)',
                        border: '1px solid rgba(59,130,246,0.2)',
                        borderRadius: '8px',
                      }}
                    />
                    <Legend />
                    <Bar dataKey="present" name="حاضر" fill="#22c55e" />
                    <Bar dataKey="absent" name="غائب" fill="#ef4444" />
                  </BarChart>
                </ResponsiveContainer>
              </GlassCard>
            </div>

            {/* Line Chart - Trend */}
            <GlassCard>
              <h3 className="text-lg font-semibold text-glass-text mb-4">
                اتجاه الحضور (آخر 7 أيام)
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={attendanceHistory}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="date" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(8,14,26,0.7)',
                      border: '1px solid rgba(59,130,246,0.2)',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="present"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    name="حاضرين"
                    dot={{ fill: '#3b82f6' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="absent"
                    stroke="#ef4444"
                    strokeWidth={2}
                    name="غائبين"
                    dot={{ fill: '#ef4444' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </GlassCard>
          </>
        )}
      </div>
    </div>
  )
}
