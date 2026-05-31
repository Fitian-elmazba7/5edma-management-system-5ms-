/**
 * Environment detection and configuration
 */

export function isElectron(): boolean {
  return typeof window !== 'undefined' && window.electronAPI !== undefined
}

export function isWeb(): boolean {
  return !isElectron()
}

export function isProduction(): boolean {
  return process.env.NODE_ENV === 'production'
}

export function isDevelopment(): boolean {
  return process.env.NODE_ENV === 'development'
}

export function getEnvironmentInfo() {
  return {
    isElectron: isElectron(),
    isWeb: isWeb(),
    isProduction: isProduction(),
    isDevelopment: isDevelopment(),
    userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'unknown',
  }
}

export type Environment = 'electron' | 'web'

export function getEnvironment(): Environment {
  return isElectron() ? 'electron' : 'web'
}
