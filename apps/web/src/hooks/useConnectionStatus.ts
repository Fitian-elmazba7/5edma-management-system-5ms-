import { useState, useEffect } from 'react'
import { useElectronAPI } from './useElectronAPI'

interface ConnectionStatus {
  isOnline: boolean
  pendingOperations: number
  isSyncing: boolean
}

/**
 * Hook to track network connection and sync status
 * In Electron: checks for pending SQLite operations
 * In Web: checks navigator.onLine
 */
export function useConnectionStatus() {
  const { isElectron, sync } = useElectronAPI()
  const [status, setStatus] = useState<ConnectionStatus>({
    isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
    pendingOperations: 0,
    isSyncing: false,
  })

  useEffect(() => {
    const handleOnline = () => setStatus((s) => ({ ...s, isOnline: true }))
    const handleOffline = () => setStatus((s) => ({ ...s, isOnline: false }))

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  useEffect(() => {
    if (!isElectron) return

    // Check for pending operations every 5 seconds
    const interval = setInterval(async () => {
      try {
        const result = await sync.getPendingOperations()
        if (result.success) {
          setStatus((s) => ({
            ...s,
            pendingOperations: result.data?.length || 0,
          }))

          // Auto-drain queue if online
          if (status.isOnline && result.data?.length > 0) {
            setStatus((s) => ({ ...s, isSyncing: true }))
            await sync.drainQueue()
            setStatus((s) => ({ ...s, isSyncing: false }))
          }
        }
      } catch (err) {
        console.error('[Connection] Error checking pending operations:', err)
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [isElectron, sync, status.isOnline])

  return status
}

/**
 * Component to display connection status
 * Shows offline indicator and pending sync count
 */
export function ConnectionStatusIndicator() {
  const { isOnline, pendingOperations, isSyncing } = useConnectionStatus()

  if (isOnline && pendingOperations === 0) {
    return null
  }

  return (
    <div
      className={`fixed bottom-4 right-4 glass-card p-3 text-sm flex items-center gap-2 ${
        isOnline ? 'border-amber-500/50' : 'border-red-500/50'
      }`}
    >
      <div
        className={`w-2 h-2 rounded-full ${
          isSyncing ? 'bg-blue-400 animate-pulse' : isOnline ? 'bg-green-400' : 'bg-red-400'
        }`}
      />
      <span className="text-gray-300">
        {!isOnline
          ? 'Offline mode'
          : isSyncing
            ? `Syncing ${pendingOperations} changes...`
            : `${pendingOperations} pending`}
      </span>
    </div>
  )
}
