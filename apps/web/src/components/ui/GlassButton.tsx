import { ReactNode } from 'react'
import { cn } from '../../lib/utils'

interface GlassButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  onClick?: () => void
  className?: string
  loading?: boolean
  fullWidth?: boolean
}

const variantStyles = {
  primary: 'glass-button-primary',
  secondary: 'glass-button-secondary',
  danger: 'glass-button-danger',
  success: 'glass-button-success',
}

const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
}

export default function GlassButton({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  type = 'button',
  onClick,
  className,
  loading = false,
  fullWidth = false,
}: GlassButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={cn(
        'glass-button',
        variantStyles[variant],
        sizeStyles[size],
        fullWidth && 'w-full',
        className,
      )}
    >
      {loading ? 'جاري...' : children}
    </button>
  )
}
