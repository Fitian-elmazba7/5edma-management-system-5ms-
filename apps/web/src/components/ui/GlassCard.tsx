import { ReactNode } from 'react'
import { cn } from '../../lib/utils'

interface GlassCardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

export default function GlassCard({
  children,
  className,
  onClick,
  hoverable = false,
}: GlassCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'glass-card',
        hoverable && 'cursor-pointer hover:shadow-lg hover:shadow-blue-500/20 transition-all',
        className,
      )}
    >
      {children}
    </div>
  )
}
