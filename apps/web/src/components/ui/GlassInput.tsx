import { InputHTMLAttributes, ReactNode } from 'react'
import { cn } from '../../lib/utils'

interface GlassInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  icon?: ReactNode
  variant?: 'default' | 'search'
}

export default function GlassInput({
  label,
  error,
  icon,
  variant = 'default',
  className,
  ...props
}: GlassInputProps) {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-sm font-medium text-glass-text">{label}</label>}
      <div className="relative">
        {icon && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-glass-muted">
            {icon}
          </div>
        )}
        <input
          className={cn(
            'glass-input',
            icon && 'pr-10',
            error && 'border-red-500/50 focus:ring-red-500/50',
            className,
          )}
          {...props}
        />
      </div>
      {error && <span className="text-sm text-red-400">{error}</span>}
    </div>
  )
}
