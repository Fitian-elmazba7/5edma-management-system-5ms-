import { ReactNode } from 'react'
import { cn } from '../../lib/utils'

interface StatCardProps {
  icon: ReactNode
  label: string
  value: string | number
  trend?: {
    value: number
    direction: 'up' | 'down'
    label?: string
  }
  color?: 'primary' | 'success' | 'warning' | 'danger'
  className?: string
}

const colorStyles = {
  primary: {
    bg: 'from-blue-600 to-blue-400',
    text: 'text-blue-300',
  },
  success: {
    bg: 'from-green-600 to-green-400',
    text: 'text-green-300',
  },
  warning: {
    bg: 'from-amber-600 to-amber-400',
    text: 'text-amber-300',
  },
  danger: {
    bg: 'from-red-600 to-red-400',
    text: 'text-red-300',
  },
}

export default function StatCard({
  icon,
  label,
  value,
  trend,
  color = 'primary',
  className,
}: StatCardProps) {
  const colors = colorStyles[color]

  return (
    <div className={cn('stat-card', className)}>
      <div className="flex items-start justify-between">
        <div className={cn('stat-icon', colors.text)}>{icon}</div>
        {trend && (
          <div className="text-xs font-medium">
            {trend.direction === 'up' ? '↑' : '↓'} {trend.value}%
          </div>
        )}
      </div>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      {trend?.label && (
        <div className="text-xs text-glass-muted mt-2">{trend.label}</div>
      )}
    </div>
  )
}
