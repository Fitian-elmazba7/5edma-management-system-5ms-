import { ReactNode } from 'react'
import { Child } from '@5edma/shared'
import { cn } from '../../lib/utils'

interface ChildCardProps {
  child: Child
  actions?: ReactNode
  onClick?: () => void
  selected?: boolean
}

// Get initials from name
function getInitials(name: string): string {
  return name
    .split(' ')
    .slice(0, 2)
    .map((n) => n[0])
    .join('')
    .toUpperCase()
}

// Get color based on class
function getClassColor(className: string): string {
  const colors: Record<string, string> = {
    'الصف الأول': 'from-blue-600 to-blue-400',
    'الصف الثاني': 'from-purple-600 to-purple-400',
    'الصف الثالث': 'from-green-600 to-green-400',
  }
  return colors[className] || 'from-indigo-600 to-indigo-400'
}

export default function ChildCard({
  child,
  actions,
  onClick,
  selected = false,
}: ChildCardProps) {
  const initials = getInitials(child.name)
  const colorClass = getClassColor(child.class)

  return (
    <div
      onClick={onClick}
      className={cn(
        'child-card group',
        selected && 'ring-2 ring-blue-500',
        onClick && 'cursor-pointer',
      )}
    >
      <div className={cn('child-avatar bg-gradient-to-br', colorClass)}>
        {initials}
      </div>

      <div className="child-info flex-1 min-w-0">
        <div className="child-name truncate">{child.name}</div>
        <div className="child-class">{child.code}</div>
        <div className="mt-2 flex gap-2 flex-wrap">
          <span className="text-xs px-2 py-1 rounded bg-blue-500/20 text-blue-300">
            {child.class}
          </span>
          {child.region && (
            <span className="text-xs px-2 py-1 rounded bg-purple-500/20 text-purple-300">
              {child.region}
            </span>
          )}
        </div>
      </div>

      {actions && (
        <div className="opacity-0 group-hover:opacity-100 transition-opacity flex flex-col gap-1">
          {actions}
        </div>
      )}
    </div>
  )
}
