import { useCallback } from 'react'

/**
 * Hook to access Electron API in renderer process
 * Only available in Electron environment
 */
export function useElectronAPI() {
  const isElectron = useCallback(() => {
    return typeof window !== 'undefined' && window.electronAPI !== undefined
  }, [])

  const openFile = useCallback(async (options: any) => {
    if (!isElectron()) throw new Error('Not in Electron environment')
    return window.electronAPI.openFile(options)
  }, [isElectron])

  const saveFile = useCallback(async (options: any) => {
    if (!isElectron()) throw new Error('Not in Electron environment')
    return window.electronAPI.saveFile(options)
  }, [isElectron])

  // Database operations for offline mode
  const database = useCallback(
    () => ({
      getChildren: async () => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.getChildren()
      },
      getChild: async (code: string) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.getChild(code)
      },
      addChild: async (child: any) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.addChild(child)
      },
      updateChild: async (code: string, updates: any) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.updateChild(code, updates)
      },
      deleteChild: async (code: string) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.deleteChild(code)
      },
      recordAttendance: async (code: string, date: string, time: string) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.recordAttendance(code, date, time)
      },
      getAttendance: async (date: string) => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.db.getAttendance(date)
      },
    }),
    [isElectron],
  )

  // Sync operations
  const sync = useCallback(
    () => ({
      getPendingOperations: async () => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.sync.getPendingOperations()
      },
      drainQueue: async () => {
        if (!isElectron()) throw new Error('Not in Electron environment')
        return window.electronAPI.sync.drainQueue()
      },
    }),
    [isElectron],
  )

  // App info
  const getAppPath = useCallback(async () => {
    if (!isElectron()) throw new Error('Not in Electron environment')
    return window.electronAPI.app.getAppPath()
  }, [isElectron])

  return {
    isElectron: isElectron(),
    openFile,
    saveFile,
    database: database(),
    sync: sync(),
    getAppPath,
  }
}

// Add type declaration for window.electronAPI
declare global {
  interface Window {
    electronAPI: {
      openFile: (options: any) => Promise<any>
      saveFile: (options: any) => Promise<any>
      db: {
        getChildren: () => Promise<any>
        getChild: (code: string) => Promise<any>
        addChild: (child: any) => Promise<any>
        updateChild: (code: string, updates: any) => Promise<any>
        deleteChild: (code: string) => Promise<any>
        recordAttendance: (code: string, date: string, time: string) => Promise<any>
        getAttendance: (date: string) => Promise<any>
      }
      sync: {
        getPendingOperations: () => Promise<any>
        drainQueue: () => Promise<any>
      }
      app: {
        getAppPath: () => Promise<any>
      }
    }
  }
}
